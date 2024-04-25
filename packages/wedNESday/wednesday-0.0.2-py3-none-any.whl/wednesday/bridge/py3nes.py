from wednesday.ports import CPU6502Bridge
from wednesday.emulators.py3nes.cpu import CPU
from wednesday.emulators.py3nes.status import Status
from wednesday.emulators.py3nes.memory_owner import MemoryOwnerMixin

from typing import List
import numpy as np

KB = 1024

FLAGS = {
    'C': Status.StatusTypes.carry,
    'Z': Status.StatusTypes.zero,
    'I': Status.StatusTypes.interrupt,
    'D': Status.StatusTypes.decimal,
    'U': Status.StatusTypes.unused1,
    'U': Status.StatusTypes.unused2,
    'V': Status.StatusTypes.overflow,
    'N': Status.StatusTypes.negative,
}


class BigEmptyRAM(MemoryOwnerMixin, object):
    memory_start_location = 0x0
    memory_end_location = 0xFFFF

    def __init__(self):
        self.memory = [0] * 64 * KB

    def get_memory(self) -> List[int]:
        return self.memory


class Py3nesCPUBridge(CPU6502Bridge):
    def start(self):
        self.memory = BigEmptyRAM()
        self.cpu = CPU(self.memory, None, None)
        self.cpu.start_up()
        self.cycles = 0

    def cpu_pc(self, counter):
        self.cpu.pc_reg = np.uint16(counter)

    def memory_set(self, pos, val):
        self.cpu.set_memory(pos, val)

    def memory_fetch(self, pos):
        return self.cpu.get_memory(pos)

    def execute(self):
        self.cpu.identify()
        self.cpu.execute()
        self.cycles += 0
        return self.cycles, None

    def cpu_set_register(self, register, value):
        if register == 'P':
            self.cpu.status_reg.from_int(value, [])
        else:
            reg = register.lower()
            setattr(self.cpu, f'{reg}_reg', np.uint8(value))

    def cpu_register(self, register):
        if register == 'P':
            return self.cpu.status_reg.to_int()
        reg = register.lower()
        return getattr(self.cpu, f'{reg}_reg')

    def cpu_flag(self, flag):
        fg = FLAGS.get(flag)
        return self.cpu.status_reg.bits[fg]

    def cpu_set_flag(self, flag):
        fg = FLAGS.get(flag)
        self.cpu.status_reg.bits[fg] = True

    def cpu_unset_flag(self, flag):
        fg = FLAGS.get(flag)
        self.cpu.status_reg.bits[fg] = False

    def cpu_push_byte(self, byte):
        self.cpu.set_stack_value(byte, 1)

    def cpu_pull_byte(self):
        return self.cpu.get_stack_value(1)

    def cpu_push_word(self, word):
        hi, lo = divmod(word, 0x100)
        self.cpu_push_byte(hi)
        self.cpu_push_byte(lo)

    def cpu_pull_word(self):
        b1 = self.cpu_pull_byte()
        b2 = self.cpu_pull_byte() << 8
        return b1 + b2
