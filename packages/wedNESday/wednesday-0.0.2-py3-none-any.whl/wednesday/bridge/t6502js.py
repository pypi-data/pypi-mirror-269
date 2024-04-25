from wednesday.ports import CPU6502Bridge
from py_mini_racer.py_mini_racer import MiniRacer
from os.path import abspath, dirname, join


here = abspath(dirname(__file__))
script = join(here, '..', '6502js_cpu.js')


class Torlus6502CPUBridge(CPU6502Bridge):
    __context = None

    @property
    def ctx(self):
        if self.__context is None:
            self.STACK_PAGE = 0x100
            with open(script) as f:
                javascript = f.read()
            self.__context = MiniRacer()
            self.__context.eval('var mem = [];')
            self.__context.eval(javascript)
        return self.__context

    def start(self):
        code = """
            var mem = Array.apply(
                null, Array(600)
            ).map(Number.prototype.valueOf,0);
        """
        self.ctx.eval(code)
        self.ctx.eval('cpu = new CPU6502()')
        self.ctx.eval('cpu.reset()')

    def cpu_pc(self, counter):
        self.ctx.eval('cpu.PC = %s' % counter)

    def memory_set(self, pos, val):
        self.ctx.eval('mem[%s] = %s' % (pos, val))

    def memory_fetch(self, pos):
        return self.ctx.eval('mem[%s]' % pos)

    def execute(self):
        self.ctx.eval('cpu.step()')
        cycles = self.ctx.eval('cpu.cycles')
        self.ctx.eval('cpu.cycles = 0')
        return cycles, None

    def cpu_set_register(self, register, value):
        if register == 'SP':
            register = 'S'
        if register == 'P':
            self.ctx.eval('cpu.C = %s' % [0, 1][0 != value & 1])
            self.ctx.eval('cpu.Z = %s' % [0, 1][0 != value & 2])
            self.ctx.eval('cpu.I = %s' % [0, 1][0 != value & 4])
            self.ctx.eval('cpu.D = %s' % [0, 1][0 != value & 8])
            self.ctx.eval('cpu.V = %s' % [0, 1][0 != value & 64])
            self.ctx.eval('cpu.N = %s' % [0, 1][0 != value & 128])
            return
        self.ctx.eval('cpu.%s = %s' % (register, value))

    def cpu_register(self, register):
        if register == 'SP':
            register = 'S'
        return self.ctx.eval('cpu.%s' % register)

    def cpu_flag(self, flag):
        return bool(self.ctx.eval('cpu.%s' % flag))

    def cpu_set_flag(self, flag):
        self.ctx.eval('cpu.%s = 1' % flag)

    def cpu_unset_flag(self, flag):
        self.ctx.eval('cpu.%s = 0' % flag)

    def cpu_push_byte(self, byte):
        stack_pointer = self.ctx.eval('cpu.S')
        self.ctx.eval('mem[%s] = %s' % (self.STACK_PAGE + stack_pointer, byte))
        self.ctx.eval('cpu.S = %s' % ((stack_pointer - 1) % 0x100))

    def cpu_pull_byte(self):
        stack_pointer = (self.ctx.eval('cpu.S') + 1) % 0x100
        self.ctx.eval('cpu.S = %s' % stack_pointer)
        return self.ctx.eval('mem[%s]' % (self.STACK_PAGE + stack_pointer))

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        b1 = self.cpu_pull_byte()
        b2 = self.cpu_pull_byte() << 8
        return b1 + b2
