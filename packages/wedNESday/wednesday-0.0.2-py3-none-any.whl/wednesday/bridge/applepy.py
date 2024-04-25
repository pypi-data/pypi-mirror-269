from wednesday.ports import CPU6502Bridge
from wednesday.emulators.applepy.cpu import CPU, BasicMemory


REGISTERS = {
    'A': 'accumulator',
    'X': 'x_index',
    'Y': 'y_index',
    'SP': 'stack_pointer',
    'PC': 'program_counter',
}

FLAGS = {
    'C': 'carry_flag',
    'Z': 'zero_flag',
    'I': 'interrupt_disable_flag',
    'D': 'decimal_mode_flag',
    'B': 'break_flag',
    'V': 'overflow_flag',
    'N': 'sign_flag',
}


class ApplepyCPUBridge(CPU6502Bridge):
    def start(self):
        class Options:
            def __init__(self):
                self.rom = None
                self.ram = None
                self.bus = None
                self.pc = 0xFFFA

        self.memory = BasicMemory()
        self.options = Options()
        self.cpu = CPU(self.options, self.memory)
        self.executor = self.cpu.run()

    def cpu_pc(self, counter):
        self.cpu.program_counter = counter

    def memory_set(self, pos, val):
        self.memory._mem[pos] = val

    def memory_fetch(self, pos):
        return self.memory._mem[pos]

    def execute(self):
        cycle, _ = next(self.executor)
        return cycle, _

    def cpu_set_register(self, register, value):
        if register == 'P':
            return self.cpu.status_from_byte(value)
        name = REGISTERS[register]
        setattr(self.cpu, name, value)

    def cpu_register(self, register):
        if register == 'P':
            return self.cpu.status_as_byte()
        name = REGISTERS[register]
        return getattr(self.cpu, name)

    def cpu_flag(self, flag):
        name = FLAGS[flag]
        return not not getattr(self.cpu, name)

    def cpu_set_flag(self, flag):
        name = FLAGS[flag]
        setattr(self.cpu, name, True)

    def cpu_unset_flag(self, flag):
        name = FLAGS[flag]
        setattr(self.cpu, name, False)

    def cpu_push_byte(self, byte):
        self.cpu.push_byte(byte)

    def cpu_pull_byte(self):
        return self.cpu.pull_byte()

    def cpu_push_word(self, word):
        self.cpu.push_word(word)

    def cpu_pull_word(self):
        return self.cpu.pull_word()
