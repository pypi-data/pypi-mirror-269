from wednesday.ports import CPU6502Bridge
from nes.pycore.mos6502 import MOS6502
from nes.pycore.memory import BigEmptyRAM


class PyntendoCPUBridge(CPU6502Bridge):
    def start(self):
        self.memory = BigEmptyRAM()
        self.cpu = MOS6502(
            memory=self.memory,
            undocumented_support_level=2,  # a few NES games make use of some more common undocumented instructions
            stack_underflow_causes_exception=False,
            support_BCD=True,
        )
        self.cpu.reset()
        self.cpu.started = True

    def cpu_pc(self, counter):
        self.cpu.PC = counter

    def memory_set(self, pos, val):
        self.memory.write(pos, val)

    def memory_fetch(self, pos):
        return self.memory.read(pos)

    def execute(self):
        cycles = self.cpu.run_next_instr()
        return cycles, None

    def cpu_set_register(self, register, value):
        if register == 'P':
            self.cpu._status_from_byte(value)
        else:
            setattr(self.cpu, register, value)

    def cpu_register(self, register):
        if register == 'P':
            return self.cpu._status_to_byte()
        return getattr(self.cpu, register)

    def cpu_flag(self, flag):
        return getattr(self.cpu, flag)

    def cpu_set_flag(self, flag):
        setattr(self.cpu, flag, True)

    def cpu_unset_flag(self, flag):
        setattr(self.cpu, flag, False)

    def cpu_push_byte(self, byte):
        self.cpu.push_stack(byte)

    def cpu_pull_byte(self):
        return self.cpu.pop_stack()

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        b1 = self.cpu_pull_byte()
        b2 = self.cpu_pull_byte() << 8
        return b1 + b2
