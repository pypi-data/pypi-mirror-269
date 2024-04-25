from typing import Any
from unittest import TestCase, skip

from wednesday.bridge.pyntendo import PyntendoCPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec


class PyntendoCPUTest(PyntendoCPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.start()

    def assertEqual(self, first: Any, second: Any, msg: Any = None) -> None:
        self.cpu.print_status()
        print('Memory' + ('==' * 10))
        self.memory.print(0x080, 16)
        print('\n')
        self.memory.print(0x100, 16)
        print('\n')
        return super().assertEqual(first, second, msg)

    @skip('TODO:')
    def test_plp(self):
        pass

    @skip('TODO')
    def test_jsr_with_illegal_opcode(self):
        pass

    @skip('TODO:')
    def test_plp(self):
        pass
