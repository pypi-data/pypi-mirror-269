from unittest import TestCase, skip
from wednesday.bridge.t6502js import Torlus6502CPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec


class Torlus6502Test(Torlus6502CPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.start()

    @skip('TODO')
    def test_jsr(self):
        pass

    @skip('TODO')
    def test_pla(self):
        pass

    @skip('TODO')
    def test_pla_n_flag_set(self):
        pass

    @skip('TODO')
    def test_pla_z_flag_set(self):
        pass

    @skip('TODO')
    def test_plp(self):
        pass

    @skip('TODO')
    def test_rti(self):
        pass

    @skip('TODO')
    def test_rts(self):
        pass

    @skip('TODO')
    def test_jsr_stack_pointer(self):
        pass

    @skip('TODO')
    def test_jsr_with_illegal_opcode(self):
        pass
