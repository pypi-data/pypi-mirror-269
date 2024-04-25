from unittest import TestCase
from unittest import skip

from wednesday.bridge.applepy import ApplepyCPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec, skip_cycles


class ApplepyCPUTest(ApplepyCPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.start()

    @skip('TODO')
    def test_adc_immediate_with_bcd(self):
        pass

    @skip('TODO:')
    def test_brk(self):
        pass

    @skip('TODO')
    def test_sbc_immediate_with_bcd(self):
        pass

    @skip('TODO')
    def test_jsr(self):
        pass

    @skip('TODO')
    def test_jsr_stack_pointer(self):
        pass

    @skip('TODO')
    def test_jsr_with_illegal_opcode(self):
        pass

    @skip('TODO')
    def test_plp(self):
        pass

    @skip_cycles
    def test_bcc(self):
        super().test_bcc()

    @skip_cycles
    def test_lda_absolute_x_2(self):
        super().test_lda_absolute_x_2()

    @skip_cycles
    def test_lda_absolute_y(self):
        super().test_lda_absolute_y()

    @skip_cycles
    def test_lda_indirect_y(self):
        super().test_lda_indirect_y()
