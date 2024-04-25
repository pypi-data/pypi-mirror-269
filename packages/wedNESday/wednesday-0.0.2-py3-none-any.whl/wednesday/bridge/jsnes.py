from wednesday.ports import CPU6502Bridge
from py_mini_racer.py_mini_racer import MiniRacer
from os.path import abspath, dirname, join

here = abspath(dirname(__file__))
jsnes_js = abspath(join(here, '..', 'jsnes_cpu.js'))
mock_interfaces = """
function require(path) {
    return null;
};

var MMAP = function(mem) {
    this.mem = mem;
};

MMAP.prototype.load = function (addr) {
    return this.mem[addr];
};

MMAP.prototype.write = function (addr, val) {
    this.mem[addr] = val;
};

var NES = function(mmap) {
    this.mmap = mmap;
};

NES.prototype.stop = function () {
};

var module = {
    exports: null
};
"""

REGISTER_MAP = {
    'PC': 'REG_PC',
    'SP': 'REG_SP',
    'A': 'REG_ACC',
    'X': 'REG_X',
    'Y': 'REG_Y',
}

FLAG_MAP = {
    'C': 'F_CARRY',
    'Z': 'F_ZERO',
    'I': 'F_INTERRUPT',
    'D': 'F_DECIMAL',
    'V': 'F_OVERFLOW',
    'N': 'F_SIGN',
}


class JsnesCPUBridge(CPU6502Bridge):
    __context = None

    @property
    def ctx(self):
        if self.__context is None:
            with open(jsnes_js) as f:
                javascript = f.read()
            self.__context = MiniRacer()
            self.__context.eval(mock_interfaces)
            self.__context.eval(javascript)

        return self.__context

    def start(self):
        code = """
            var mem = Array.apply(
                null, Array(600)
            ).map(Number.prototype.valueOf,0);

            var mmap = new MMAP(mem);
            var nes = new NES(mmap);
            var cpu = new CPU(nes);
            cpu.reset();
            cpu.mem = mem;
        """
        self.ctx.eval(code)

    def cpu_pc(self, counter):
        self.ctx.eval(f'cpu.REG_PC = {counter - 1};')
        self.ctx.eval(f'cpu.REG_PC_NEW = {counter - 1};')

    def memory_set(self, pos, val):
        # self.ctx.eval(f'mmap.mem[{pos}] = {val};')
        self.ctx.eval(f'cpu.mem[{pos}] = {val};')

    def memory_fetch(self, pos):
        if pos < 0x2000:
            return self.ctx.eval(f'cpu.mem[{pos}];')
        else:
            return self.ctx.eval(f'mmap.mem[{pos}];')

    def execute(self):
        cycles = self.ctx.eval('cpu.emulate();')
        return cycles, None

    def cpu_set_register(self, register, value):
        reg = REGISTER_MAP.get(register)
        if reg:
            self.ctx.eval(f'cpu.{reg} = {value};')
        elif register == 'P':
            self.ctx.eval(f'cpu.setStatus({value});')
        else:
            raise NotImplementedError(f'Unknow Register: {register}')

    def cpu_register(self, register):
        reg = REGISTER_MAP.get(register)
        if reg:
            val = self.ctx.eval(f'cpu.{reg};')
            if register == 'PC':
                return val + 1
            return val
        else:
            raise NotImplementedError(f'Unknow Register: {register}')

    def cpu_flag(self, flag):
        fg = FLAG_MAP.get(flag)
        if fg:
            val = bool(self.ctx.eval(f'cpu.{fg};'))
            if flag in ['Z']:
                return not val   # TODO: check this
            return val
        else:
            raise NotImplementedError(f'Unknow Flag: {flag}')

    def cpu_set_flag(self, flag):
        fg = FLAG_MAP.get(flag)
        if fg:
            self.ctx.eval(f'cpu.{fg} = 1;')
        else:
            raise NotImplementedError(f'Unknow Flag: {flag}')

    def cpu_unset_flag(self, flag):
        fg = FLAG_MAP[flag]
        if fg:
            self.ctx.eval(f'cpu.{fg} = 0;')
        else:
            raise NotImplementedError(f'Unknow Flag: {flag}')

    def cpu_push_byte(self, byte):
        self.ctx.eval(f'cpu.push({byte})')

    def cpu_pull_byte(self):
        return self.ctx.eval('cpu.pull()')

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        b1 = self.cpu_pull_byte()
        b2 = self.cpu_pull_byte() << 8
        return b1 + b2
