import os, re, csv, struct, array, collections, struct, yaml, importlib.resources, pathlib

try:
    base = pathlib.Path('.') if pathlib.Path('tinyrv_opcodes').exists() else importlib.resources.files('tinyrv')
    opcodes = yaml.safe_load(open(base / 'tinyrv_opcodes/instr_dict.yaml'))
    for aname, op in opcodes.items(): op['name'] = aname
    mask_match = [(int(op['mask'], 16), int(op['match'], 16), op) for op in opcodes.values()]
    def dr(h,l): return list(range(h,l-1,-1))
    arg_bits = dict((a, dr(int(h),int(l))) for a, h, l in csv.reader(open(base / 'tinyrv_opcodes/arg_lut.csv'), skipinitialspace=True))
    for s in open(base / 'tinyrv_opcodes/constants.py').readlines():  # immediate scrambling from latex_mapping. Some better way?
        if m := re.match(r"latex_mapping\[['\"](.*?)['\"]\] = ['\"][^\[]*\[([^\]]*)\]['\"]", s):
            fbits = sum([(dr(*(int(i) for i in part.split(':'))) if ':' in part else [int(part)]) for part in m[2].split('$\\\\vert$')], [])
            locs = [-1] * (max(fbits)+1)
            for i, b in enumerate(fbits): locs[-b-1] = arg_bits[m[1]][i]
            arg_bits[m[1]] = [31] * (32-len(locs)) + locs if locs[0] == 31 else locs  # sign extension
    csrs = dict((int(a, 16), n) for fn in ['tinyrv_opcodes/csrs.csv', 'tinyrv_opcodes/csrs32.csv'] for a, n in csv.reader(open(base / fn), skipinitialspace=True))
    csrs_addrs = dict((n, a) for a, n in csrs.items())
    iregs = 'zero,ra,sp,gp,tp,t0,t1,t2,fp,s1,a0,a1,a2,a3,a4,a5,a6,a7,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,t3,t4,t5,t6'.split(',')
    st = 'sb,sh,sw,sd'.split(','); ldst = 'lb,lh,lw,ld,lbu,lhu,lwu'.split(',') + st
    fence_flags = ',w,r,rw,o,ow,or,orw,i,iw,ir,irw,io,iow,ior,iorw'.split(',')
    customs = {0b0001011: 'custom0', 0b0101011: 'custom1', 0b1011011: 'custom2', 0b1111011: 'custom3'}  # RISC-V spec ch. 34, table 70
except Exception as e: raise Exception("Unable to load RISC-V specs. Do:\n"
                                       "git clone https://github.com/riscv/riscv-opcodes.git tinyrv_opcodes\n"
                                       "cd tinyrv_opcodes; make")

def xfmt(d, xlen): return f'{{:0{xlen//4}x}}'.format(d&((1<<xlen)-1))

class rvop:
    def __init__(self, **kwargs): [setattr(self, k, v) for k, v in kwargs.items()]
    def arg_str(self):
        args = [None]*4
        for k, v in self.args.items():  # hand-coded argument formats
            k = k.replace('c_','').replace('_n0','')
            if k == 'pred': args[0] = fence_flags[v]
            elif k == 'succ': args[1] = fence_flags[v]
            elif self.name == 'fence' and k != 'fm': pass
            elif self.name.startswith('c.') or self.name.startswith('f'): args.append(f'{k}={v}')  # TODO: compressed and fp registers
            elif k == 'rd': args[0] = iregs[v]
            elif k == 'csr': args[1] = csrs.get(v, hex(v))
            elif k == 'rs1': args[2] = f"{self.args['imm12']}({iregs[v]})" if self.name in ldst + ['jalr'] else iregs[v]
            elif k == 'rs2': args[3] = iregs[v]
            elif k in ['imm12', 'zimm']: args.append(f'{v}' if self.name not in ldst + ['jalr'] else None)
            elif k in ['jimm20', 'bimm12']: args.append(xfmt(self.addr+v, 32))
            elif k in ['imm20']: args.append(xfmt(v, 32))
            elif 'sham' in k: args.append(f'{v}')
            else: args.append(f'{k}={v}')  # fallback
        args = args[::-1] if self.name in st else args  # snowflake sb/sh/sw/sd arg order: <src>, <dst>
        return ', '.join([a for a in args if a is not None])
    def valid(self): return min([not('nz' in k or 'n0' in k) or v!=0 for k, v in self.args.items()] + [hasattr(self, 'extension')])
    def __repr__(self): return f'{self.name.replace("_","."):10} {self.arg_str()}'

def rvsplitter(*data, base=0):  # yields addresses and 32-bit/16-bit(compressed) RISC-V instruction words.
    lower16 = 0
    for addr, instr in enumerate(struct.iter_unpack('<H', (open(data[0],'rb').read() if isinstance(data[0],str) and os.path.isfile(data[0]) else 
                    array.array('I',[int(d,16) if isinstance(d,str) else d for d in (data[0] if hasattr(data[0], '__iter__') and not isinstance(data[0],str) else data)])))):
        if lower16:
            yield int(base)+(addr-1)*2, (instr[0]<<16)|lower16
            lower16 = 0
        elif instr[0]&3 == 3: lower16 = instr[0]  # Two LSBs set: 32-bit instruction
        else: yield int(base)+addr*2, instr[0]

def rvdecoder(*data, base=0):  # yields decoded ops.
    for addr, instr in rvsplitter(*data, base=base):
        if instr == 0: continue  # RV-spec: 0x0 is invalid - skip
        o = rvop(addr=addr, data=instr, name=customs.get(instr&0b1111111,'UNKNOWN'), args={'raw':f'0x{instr:08x}'})
        for mask, match, op in mask_match:
            if instr&mask == match:
                args = collections.defaultdict(int)
                for vf in op['variable_fields']:
                    value = 0
                    for bit in arg_bits[vf]: value = (value << 1) | ((instr>>bit)&1 if bit>=0 else 0)
                    vf = vf.replace('hi','').replace('lo','').replace('c_','')
                    args[vf] |= value-(1<<32) if value&(1<<31) else value
                    if '_p' in vf: args[vf.replace('_p','')] = args[vf]+8  # reg aliases for some compressed instructions
                    if '_n0' in vf: args[vf.replace('_n0','')] = args[vf]
                [setattr(o,k,v) for k,v in (op|args).items()]
                o.args = dict(args)
                break
        yield o

def rvprint(*data, base=0, xlen=64):  # prints listing of decoded instructions.
    for op in rvdecoder(*data, base=base): print(f'{xfmt(op.addr,32)}: {str(op):40} # {", ".join(op.extension) if op.valid() else "INVALID"}')

class rvmem:
    def __init__(self, xlen=64):
        self.psize, self.pages, self.xlen = 2<<12, {}, xlen
        self.fmt_sizes = {'q': 8, 'Q': 8, 'i': 4, 'I': 4, 'h': 2, 'H': 2, 'b': 1, 'B': 1}
        self.trace = []
    def read(self, file, base=0): [self.store(i+base, b, 'B') for i, b in enumerate(open(file, 'rb').read())]
    def _page_pa(self, addr):
        pb, pa = addr&~(self.psize-1), addr&(self.psize-1)
        if pb not in self.pages: self.pages[pb] = bytearray(self.psize)
        return self.pages[pb], pa
    def store(self, addr, data, fmt=None):
        page, pa = self._page_pa(addr)
        fmt = fmt or ('i' if self.xlen==32 else 'q')
        page[pa:pa+self.fmt_sizes[fmt]] = struct.pack(fmt, data)
        self.trace.append(f'mem[{xfmt(addr, self.xlen)}] <- {xfmt(data, self.fmt_sizes[fmt]*8)}')
    def load(self, addr, fmt=None):
        page, pa = self._page_pa(addr)
        fmt = fmt or ('i' if self.xlen==32 else 'q')
        data = struct.unpack(fmt, page[pa:pa+self.fmt_sizes[fmt]])[0]
        self.trace.append(f'mem[{xfmt(addr, self.xlen)}] -> {xfmt(data, self.fmt_sizes[fmt]*8)}')
        return data

class rvregs:  # normal list, but ignore writes to x[0]
    def __init__(self): self._x = [0]*32
    def __getitem__(self, i): return self._x[i]
    def __setitem__(self, i, d): self._x[i] = d if i else 0

class rvsim:  # simulates RV32IZicsr_Zifencei, RV64IZicsr_Zifencei and some additional instructions
    def __init__(self, mem, xlen=64):
        self.mem, self.xlen = mem, xlen
        self.pc, self.x, self.f, self.csr = 0, rvregs(), [0]*32, [0]*4096
        self.xlenmask = (1<<self.xlen)-1
        [setattr(self, n, i) for i, n in enumerate(iregs)]
        [setattr(self, n, a) for a, n in csrs.items()]
    def __repr__(self): return '\n'.join(['  '.join([f'x{r+rr:02d}({(iregs[r+rr])[-2:]})={xfmt(self.x[r+rr], self.xlen)}' for r in range(0, 32, 8)]) for rr in range(8)])
    def addop(self, _opfn): setattr(self, _opfn.__name__, _opfn.__get__(self, rvsim))
    def sext(self,v,l=None): l = l or self.xlen; return v|~((1<<l)-1) if v&(1<<(l-1)) else v&((1<<l)-1)
    def checked_store(self, addr, rs2, fmt, mask, alignmask):
        if addr&alignmask == 0: self.mem.store(addr&self.xlenmask, self.x[rs2]&mask, fmt); self.pc += 4
        else: self.csr[self.mtval], self.csr[self.mepc], self.csr[self.mcause], self.pc = addr&self.xlenmask, self.pc, 6, self.csr[self.mtvec] & (~3) & self.xlenmask
    def checked_load (self, rd, addr, fmt, alignmask):
        if addr&alignmask == 0: self.x[rd] = self.mem.load(addr&self.xlenmask, fmt); self.pc += 4
        else: self.csr[self.mtval], self.csr[self.mepc], self.csr[self.mcause], self.pc = addr&self.xlenmask, self.pc, 4, self.csr[self.mtvec] & (~3) & self.xlenmask
    def _auipc (self, rd, imm20,  **_): self.x[rd] = self.sext(self.pc+imm20); self.pc+=4
    def _lui   (self, rd, imm20,  **_): self.x[rd] = imm20; self.pc+=4
    def _jal   (self, rd, jimm20, **_): self.x[rd] = self.pc+4; self.pc = (self.pc+jimm20)&self.xlenmask
    def _jalr  (self, rd, rs1, imm12, **_): self.x[rd], self.pc = self.pc+4, (self.x[rs1]+imm12)&self.xlenmask&(-2)  # LSB=0
    def _beq   (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1] == self.x[rs2] else self.pc+4
    def _bne   (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1] != self.x[rs2] else self.pc+4
    def _blt   (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1] < self.x[rs2] else self.pc+4
    def _bge   (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1] >= self.x[rs2] else self.pc+4
    def _bltu  (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1]&self.xlenmask < self.x[rs2]&self.xlenmask else self.pc+4
    def _bgeu  (self, rs1, rs2, bimm12, **_): self.pc = (self.pc+bimm12) if self.x[rs1]&self.xlenmask >= self.x[rs2]&self.xlenmask else self.pc+4
    def _sb    (self, rs1, rs2, imm12, **_): self.mem.store((self.x[rs1]+imm12)&self.xlenmask, self.x[rs2]&((1<<8)-1), 'B'); self.pc+=4
    def _sh    (self, rs1, rs2, imm12, **_): self.checked_store((self.x[rs1]+imm12)&self.xlenmask, rs2, 'H', (1<<16)-1, 1)
    def _sw    (self, rs1, rs2, imm12, **_): self.checked_store((self.x[rs1]+imm12)&self.xlenmask, rs2, 'I', (1<<32)-1, 3)
    def _sd    (self, rs1, rs2, imm12, **_): self.checked_store((self.x[rs1]+imm12)&self.xlenmask, rs2, 'Q', (1<<64)-1, 7)
    def _lb    (self, rd, rs1, imm12,  **_): self.x[rd] = self.mem.load((self.x[rs1]+imm12)&self.xlenmask, 'b'); self.pc+=4
    def _lh    (self, rd, rs1, imm12,  **_): self.checked_load(rd, self.x[rs1]+imm12, 'h', 1)
    def _lw    (self, rd, rs1, imm12,  **_): self.checked_load(rd, self.x[rs1]+imm12, 'i', 3)
    def _ld    (self, rd, rs1, imm12,  **_): self.checked_load(rd, self.x[rs1]+imm12, 'q', 7)
    def _lbu   (self, rd, rs1, imm12,  **_): self.x[rd] = self.mem.load((self.x[rs1]+imm12)&self.xlenmask, 'B'); self.pc+=4
    def _lhu   (self, rd, rs1, imm12,  **_): self.checked_load(rd, self.x[rs1]+imm12, 'H', 1)
    def _lwu   (self, rd, rs1, imm12,  **_): self.checked_load(rd, self.x[rs1]+imm12, 'I', 3)
    def _addi  (self, rd, rs1, imm12,  **_): self.x[rd] = self.sext(self.x[rs1] + imm12); self.pc+=4
    def _slti  (self, rd, rs1, imm12,  **_): self.x[rd] = self.x[rs1] < imm12; self.pc+=4
    def _sltiu (self, rd, rs1, imm12,  **_): self.x[rd] = (self.x[rs1]&self.xlenmask) < (self.sext(imm12, 32)&self.xlenmask); self.pc+=4
    def _xori  (self, rd, rs1, imm12,  **_): self.x[rd] = self.sext(self.x[rs1] ^ imm12); self.pc+=4
    def _ori   (self, rd, rs1, imm12,  **_): self.x[rd] = self.sext(self.x[rs1] | imm12); self.pc+=4
    def _andi  (self, rd, rs1, imm12,  **_): self.x[rd] = self.sext(self.x[rs1] & imm12); self.pc+=4
    def _slli  (self, rd, rs1, shamtd, **_): self.x[rd] = self.sext(self.x[rs1] << shamtd); self.pc+=4  # shared with RV64I
    def _srli  (self, rd, rs1, shamtd, **_): self.x[rd] = self.sext((self.x[rs1]&self.xlenmask) >> shamtd); self.pc+=4  # shared with RV64I
    def _srai  (self, rd, rs1, shamtd, **_): self.x[rd] = self.sext(self.x[rs1] >> shamtd); self.pc+=4  # shared with RV64I
    def _add   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] + self.x[rs2]); self.pc+=4
    def _sub   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] - self.x[rs2]); self.pc+=4
    def _sll   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] << (self.x[rs2]&(self.xlen-1))); self.pc+=4
    def _slt   (self, rd, rs1, rs2,    **_): self.x[rd] = self.x[rs1] < self.x[rs2]; self.pc+=4
    def _sltu  (self, rd, rs1, rs2,    **_): self.x[rd] = (self.x[rs1]&self.xlenmask) < (self.x[rs2]&self.xlenmask); self.pc+=4
    def _xor   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] ^ self.x[rs2]); self.pc+=4
    def _srl   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext((self.x[rs1]&self.xlenmask) >> (self.x[rs2]&(self.xlen-1))); self.pc+=4
    def _sra   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] >> (self.x[rs2]&(self.xlen-1))); self.pc+=4
    def _or    (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] | self.x[rs2]); self.pc+=4
    def _and   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] & self.x[rs2]); self.pc+=4  # mostly RV32I until here
    def _addiw (self, rd, rs1, imm12,  **_): self.x[rd] = self.sext(self.x[rs1] + imm12, 32); self.pc+=4  # RV64I from here
    def _slliw (self, rd, rs1, shamtw, **_): self.x[rd] = self.sext(self.x[rs1] << shamtw, 32); self.pc+=4
    def _srliw (self, rd, rs1, shamtw, **_): self.x[rd] = self.sext((self.x[rs1]&((1<<32)-1)) >> shamtw, 32); self.pc+=4
    def _sraiw (self, rd, rs1, shamtw, **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) >> shamtw, 32); self.pc+=4
    def _addw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) + self.sext(self.x[rs2], 32), 32); self.pc+=4
    def _subw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) - self.sext(self.x[rs2], 32), 32); self.pc+=4
    def _sllw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) << (self.x[rs2]&31), 32); self.pc+=4
    def _srlw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext((self.x[rs1]&((1<<32)-1)) >> (self.x[rs2]&31), 32); self.pc+=4
    def _sraw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) >> (self.x[rs2]&31), 32); self.pc+=4
    def _mul   (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.x[rs1] * self.x[rs2]); self.pc+=4  # RV32M
    def _mulw  (self, rd, rs1, rs2,    **_): self.x[rd] = self.sext(self.sext(self.x[rs1], 32) * self.sext(self.x[rs2], 32), 32); self.pc+=4  # RV64M
    def _fence (self,                  **_): self.pc+=4
    def _fence_i(self,                 **_): self.pc+=4
    def _csrrwi(self, rd, csr, zimm,   **_): self.x[rd], self.csr[csr] = self.csr[csr], zimm if (csr&0xc00)!=0xc00 else self.csr[csr]; self.pc+=4
    def _csrrs (self, rd, csr, rs1,    **_): self.x[rd], self.csr[csr] = self.csr[csr], (self.csr[csr]|self.x[rs1]) if (csr&0xc00)!=0xc00 else self.csr[csr]; self.pc+=4
    def _csrrc (self, rd, csr, rs1,    **_): self.x[rd], self.csr[csr] = self.csr[csr], (self.csr[csr]&~self.x[rs1]) if (csr&0xc00)!=0xc00 else self.csr[csr]; self.pc+=4
    def _csrrw (self, rd, csr, rs1,    **_): self.x[rd], self.csr[csr] = self.csr[csr], self.x[rs1] if (csr&0xc00)!=0xc00 else self.csr[csr]; self.pc+=4
    def _mret  (self,                  **_): self.pc = self.csr[self.mepc] & self.xlenmask
    def _ecall (self,                  **_):                                 self.csr[self.mepc] = self.pc; self.csr[self.mcause] = 11; self.pc = self.csr[self.mtvec] & (~3) & self.xlenmask
    def _ebreak(self,                  **_): self.csr[self.mtval] = self.pc; self.csr[self.mepc] = self.pc; self.csr[self.mcause] = 3;  self.pc = self.csr[self.mtvec] & (~3) & self.xlenmask
    def _c_addi(self, rd_rs1, nzimm6,  **_): self.x[rd_rs1] += nzimm6; self.pc+=2  # needed for c.nop in test rv32i_m/privilege/src/misalign-jal-01.S
    def step(self, steps=1, bpts=set()):
        for _ in range(steps):
            self.op = next(rvdecoder(self.mem.load(self.pc, 'I'), base=self.pc))
            self.mem.trace = []
            if hasattr(self, '_'+self.op.name): getattr(self, '_'+self.op.name)(**self.op.args)  # dispatch instruction
            else: print(f'{xfmt(self.op.addr, self.xlen)}: {str(self.op):40} # {self.op.extension if self.op.valid() else "UNKNOWN"}  # halted: unimplemented op'); break
            rdinfo = f'{iregs[self.op.rd]} = {xfmt(self.x[self.op.rd], self.xlen)}' if 'rd' in self.op.args and self.op.rd != 0 else ''
            print(f'{xfmt(self.op.addr, self.xlen)}: {str(self.op):40} # {rdinfo}', ' '.join(self.mem.trace))
            if self.pc-self.op.addr not in (2, 4): print()
            if self.op.addr in bpts|{self.pc}: break