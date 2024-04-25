from unittest import TestCase, skip

from wednesday.bridge.py65 import Py65CPUBridge
from wednesday.cpu_6502_spec import CPU6502Spec


class Py65CPUTest(Py65CPUBridge, CPU6502Spec, TestCase):
    def setUp(self):
        self.start()

    @skip('TODO:')
    def test_plp(self):
        pass

    @skip('TODO:')
    def test_jsr(self):
        pass

    @skip('TODO:')
    def test_jsr_stack_pointer(self):
        pass

    @skip('TODO:')
    def test_plp(self):
        pass
