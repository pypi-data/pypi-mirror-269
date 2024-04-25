from unittest import TestCase, skip
from wednesday.bridge.jsnes import JsnesCPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec, skip_cycles


class JsnesCPUTest(JsnesCPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.set_check_cycles(True)
        self.start()

    @skip_cycles
    def test_bcc(self):
        super().test_bcc()

    @skip('TODO')
    def test_beq(self):
        pass

    @skip('TODO')
    def test_bne(self):
        pass

    @skip('TODO')
    def test_brk(self):
        pass

    @skip('Not implemented on jsNES')
    def test_adc_immediate_with_bcd(self):
        pass

    @skip('TODO: check SP register')
    def test_jsr(self):
        pass

    @skip('TODO:')
    def test_jsr_stack_pointer(self):
        pass

    @skip('TODO:')
    def test_php(self):
        pass

    @skip('TODO:')
    def test_plp(self):
        pass

    @skip('TODO')
    def test_rti(self):
        pass

    @skip('TODO')
    def test_rts(self):
        pass

    @skip('TODO')
    def test_tsx(self):
        pass

    @skip('TODO')
    def test_txs(self):
        pass
