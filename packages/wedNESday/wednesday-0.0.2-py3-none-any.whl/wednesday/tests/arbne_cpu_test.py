from unittest import TestCase, skip

from wednesday.bridge.arbne import ArbneCPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec, skip_cycles


class ArbneCPUTest(ArbneCPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.start()

    @skip
    def test_plp(self):
        pass

    @skip
    def test_adc_immediate_with_bcd(self):
        pass

    @skip
    def test_bcc(self):
        pass

    @skip
    def test_brk(self):
        pass

    @skip
    def test_jsr(self):
        pass

    @skip_cycles
    def test_lda_absolute_x(self):
        super().test_lda_absolute_x()

    @skip_cycles
    def test_lda_absolute_x_2(self):
        super().test_lda_absolute_x_2()

    @skip_cycles
    def test_lda_absolute_y(self):
        super().test_lda_absolute_y()

    @skip_cycles
    def test_lda_indirect_y(self):
        super().test_lda_indirect_y()
