from unittest import skip

"""
CPU 6502 spec based on tests on Nintengo project
https://github.com/nwidger/nintengo/blob/master/m65go2/instructions_test.go
"""


def skip_cycles(func):
    def wrapper(self):
        self.set_check_cycles(False)
        func(self)

    return wrapper


class Status:
    C = 0b00000001   # Carry
    Z = 0b00000010   # Zero
    I = 0b00000100   # Interrupt Disable
    D = 0b00001000   # Decimal
    B = 0b00010000   # B Flag
    U = 0b00100000   # Unused always pushed as 1
    V = 0b01000000   # Overflow
    N = 0b10000000   # Negative


class CPU6502Spec:
    def set_check_cycles(self, check):
        self._check_cycles = check

    def check_cycles(self):
        if hasattr(self, '_check_cycles'):
            return self._check_cycles
        return True

    def cpu_pc(self, counter):
        raise NotImplementedError()

    def memory_set(self, pos, val):
        raise NotImplementedError()

    def memory_fetch(self, pos):
        raise NotImplementedError()

    def execute(self):
        raise NotImplementedError()

    def cpu_set_register(self, register, value):
        raise NotImplementedError()

    def cpu_register(self, register):
        raise NotImplementedError()

    def cpu_flag(self, flag):
        raise NotImplementedError()

    def cpu_set_flag(self, flag):
        raise NotImplementedError()

    def cpu_unset_flag(self, flag):
        raise NotImplementedError()

    def cpu_push_byte(self, byte):
        raise NotImplementedError()

    def cpu_pull_byte(self):
        raise NotImplementedError()

    def cpu_push_word(self, word):
        raise NotImplementedError()

    def cpu_pull_word(self):
        raise NotImplementedError()

    def cpu_force_interrupt(self, interrupt):
        raise NotImplementedError()

    def cpu_get_interrupt(self, interrupt):
        raise NotImplementedError()

    def execute_interrupt(self):
        raise NotImplementedError()

    def test_lda_imediate(self):
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xA9)
        self.memory_set(0x0101, 0xFF)
        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_zeropage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)
        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_zero_page_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAD)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xBD)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 4)
        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_absolute_x_2(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xBD)
        self.memory_set(0x0101, 0xFF)
        self.memory_set(0x0102, 0x02)
        self.memory_set(0x0300, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 5)

    def test_lda_absolute_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 4)
        self.assertEqual(self.cpu_register('A'), 0xFF)

        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB9)
        self.memory_set(0x0101, 0xFF)
        self.memory_set(0x0102, 0x02)
        self.memory_set(0x0300, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 5)

    def test_lda_indirect_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_lda_indirect_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 5)
        self.assertEqual(self.cpu_register('A'), 0xFF)

        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)
        self.memory_set(0x0085, 0x02)
        self.memory_set(0x0300, 0xFF)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 6)

    def test_lda_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA9)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_lda_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_lda_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA9)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_lda_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LDX

    def test_ldx_immediate(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA2)
        self.memory_set(0x0101, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_ldx_zero_page(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_ldx_zeropage_y(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_ldx_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_ldx_absolute_y(self):
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xBE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_ldx_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA2)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ldx_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA2)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ldx_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA2)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ldx_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA2)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LDY

    def test_ldy_immediate(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA0)
        self.memory_set(0x0101, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_ldy_zeropage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()
        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_ldy_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_ldy_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAC)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_ldy_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xBC)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_ldy_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA0)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ldy_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ldy_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA0)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ldy_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // STA

    def test_sta_zeropage(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x85)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_sta_zeropage_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x95)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_sta_absolute(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_sta_absolute_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x9D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_sta_absolute_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x99)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_sta_indirect_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x81)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0087), 0xFF)

    def test_sta_indirect_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x91)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0087), 0xFF)

    # // STX

    def test_stx_zeropage(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x86)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_stx_zeropage_y(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x96)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_stx_absolute(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    # // STY

    def test_sty_zeropage(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x84)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_sty_zeropage_y(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x94)
        self.memory_set(0x0101, 0x84)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_sty_absolute(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8C)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    # // TAX

    def test_tax(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAA)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_tax_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAA)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_tax_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAA)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_tax_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAA)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_tax_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xAA)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // TAY

    def test_tay(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xA8)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    # // TXA

    def test_txa(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x8A)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    # // TYA

    def test_tya(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x98)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    # // TSX

    def test_tsx(self):
        self.cpu_set_register('SP', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xBA)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    # // TXS

    def test_txs(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x9A)

        self.execute()

        self.assertEqual(self.cpu_register('SP'), 0xFF)

    # // PHA

    def test_pha(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x48)

        self.execute()

        self.assertEqual(self.cpu_pull_byte(), 0xFF)

    # // PHP

    def test_php(self):
        self.cpu_set_register('P', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x08)

        self.execute()

        self.assertEqual(self.cpu_pull_byte(), 0xFF)

    # // PLA

    def test_pla(self):
        self.cpu_pc(0x0100)
        self.cpu_push_byte(0xFF)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_pla_z_flag_set(self):
        self.cpu_push_byte(0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_pla_z_flag_unset(self):
        self.cpu_push_byte(0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_pla_n_flag_set(self):
        self.cpu_push_byte(0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()
        self.assertTrue(self.cpu_flag('N'))

    def test_pla_n_flag_unset(self):
        self.cpu_push_byte(0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x68)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // PLP

    def test_plp(self):
        self.cpu_push_byte(0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x28)

        self.execute()

        self.assertEqual(self.cpu_register('P'), 0xCF)

    # // AND

    def test_and_immediate(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_zeropage(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x25)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_zeropage_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x35)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_absolute(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_absolute_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x3D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_absolute_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x39)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_indirect_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x21)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_indirect_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x31)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x0F)

    def test_and_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_and_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_and_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_and_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x29)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // EOR

    def test_eor_immediate(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_zeropage(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x45)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_zeropage_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x55)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_absolute(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_absolute_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x5D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_absolute_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x59)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_indirect_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x41)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_indirect_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x51)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xF0)

    def test_eor_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_eor_z_flag_unset(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_eor_n_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x81)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_eor_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x49)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ORA

    def test_ora_immediate(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_zeropage(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x05)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_zeropage_x(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x15)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_absolute(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x0F)
        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_absolute_x(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x1D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_absolute_y(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x19)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_indirect_x(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x01)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_indirect_y(self):
        self.cpu_set_register('A', 0xF0)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x11)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x0F)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0xFF)

    def test_ora_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ora_z_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ora_n_flag_set(self):
        self.cpu_set_register('A', 0x81)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ora_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x09)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // BIT

    def test_bit_zeropage(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x7F)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_absolute(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2C)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x7F)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_n_flag_set(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_bit_n_flag_unset(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x7F)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_bit_v_flag_set(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_bit_v_flag_unset(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x3F)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_bit_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_bit_z_flag_unset(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x24)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x3F)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    # // ADC

    def test_adc_immediate(self):

        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_immediate_with_bcd(self):
        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29)  # BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x11)  # BCD

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x40)

        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29 | Status.N)  # BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x29)  # BCD

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x38)

        self.cpu_set_flag('D')
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x58)  # BCD
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x46)  # BCD

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x05)

    def test_adc_zeropage(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x65)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_zeropage_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x75)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_absolute(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_absolute_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x7D)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_absolute_y(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x79)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_indirect_x(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x61)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_indirect_y(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x71)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x02)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x03)

    def test_adc_c_flag_set(self):
        self.cpu_set_register('A', 0xFF)   # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xFF)   # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00)   # +0

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_adc_c_flag_unset(self):
        self.cpu_set_register('A', 0x00)   # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_unset_flag('C')
        self.cpu_set_register('A', 0xFF)   # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00)   # +0

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_adc_z_flag_set(self):
        self.cpu_set_register('A', 0x00)   # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x00)   # +0

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_adc_z_flag_unset(self):
        self.cpu_set_register('A', 0x00)   # +0
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0xFF)   # -1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_adc_v_flag_set(self):
        self.cpu_set_register('A', 0x7F)   # +127
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_adc_v_flag_unset(self):
        self.cpu_set_register('A', 0x01)   # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_adc_n_flag_set(self):
        self.cpu_set_register('A', 0x01)   # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_adc_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)   # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x69)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // SBC

    def test_sbc_immediate(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_immediate_with_bcd(self):
        self.cpu_set_flag('D')
        self.cpu_set_register('A', 0x29)   # BCD
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x11)   # BCD

        self.execute()

        # TODO: self.assertEqual(self.cpu_register('A'), 0x18)

    def test_sbc_zeroPage(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_zeropage_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_absolute(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xED)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_absolute_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xFD)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_absolute_y(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_indirect_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xE1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_indirect_y(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x02)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_sbc_c_flag_set(self):
        self.cpu_set_register('A', 0xC4)   # -60
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x3C)   # +60

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_sbc_c_flag_unset(self):
        self.cpu_set_register('A', 0x02)   # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x04)   # +4

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_sbc_z_flag_set(self):
        self.cpu_set_register('A', 0x02)   # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_sbc_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)   # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_sbc_v_flag_set(self):
        self.cpu_set_register('A', 0x80)   # -128
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('V'))

    def test_sbc_v_flag_unset(self):
        self.cpu_set_register('A', 0x01)   # +1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    def test_sbc_n_flag_set(self):
        self.cpu_set_register('A', 0xFD)   # -3
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_sbc_n_flag_unset(self):
        self.cpu_set_register('A', 0x02)   # +2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE9)
        self.memory_set(0x0101, 0x01)   # +1

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // CMP

    def test_cmp_immediate(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_zeropage(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_zeropage_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD5)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCD)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xDD)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_absolute_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD9)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_indirect_x(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x87)
        self.memory_set(0x0086, 0x00)
        self.memory_set(0x0087, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_indirect_y(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_set_register('Y', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD1)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x86)
        self.memory_set(0x0085, 0x00)
        self.memory_set(0x0087, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_n_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_cmp_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cmp_z_flag_set(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cmp_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

        self.cpu_set_register('A', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0xFF)   # -1

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cmp_c_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_register('A', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0xFD)   # s -3

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cmp_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_set_register('A', 0xFD)   # -3
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC9)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CPX

    def test_cpx_immediate(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_zeropage(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_absolute(self):
        self.cpu_set_register('X', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xEC)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_n_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_cpx_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cpx_z_flag_set(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpx_z_flag_unset(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cpx_c_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cpx_C_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CPY

    def test_cpy_immediate(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_zeroPage(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC4)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_absolute(self):
        self.cpu_set_register('Y', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCC)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFF)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_n_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_cpy_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    def test_cpy_z_flag_set(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_cpy_z_flag_unset(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_cpy_c_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_cpy_c_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC0)
        self.memory_set(0x0101, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // INC

    def test_inc_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFE)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_inc_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0xFE)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_inc_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xEE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0xFE)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0xFF)

    def test_inc_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xFE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0xFE)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0xFF)

    def test_inc_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFF)   # -1

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_inc_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_inc_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0xFE)   # -2

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_inc_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // INX

    def test_inx(self):
        self.cpu_set_register('X', 0xFE)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE8)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0xFF)

    def test_inx_z_flag_set(self):
        self.cpu_set_register('X', 0xFF)   # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE8)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_inx_z_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE8)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_inx_n_flag_set(self):
        self.cpu_set_register('X', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE8)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_inx_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xE8)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // INY

    def test_iny(self):
        self.cpu_set_register('Y', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC8)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0xFF)

    def test_iny_z_flag_set(self):
        self.cpu_set_register('Y', 0xFF)   # -1
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC8)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_iny_z_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC8)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_iny_n_flag_set(self):
        self.cpu_set_register('Y', 0xFE)   # -2
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC8)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_iny_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC8)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEC

    def test_dec_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x01)

    def test_dec_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x01)

    def test_dec_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x01)

    def test_dec_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xDE)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x01)

    def test_dec_z_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dec_z_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dec_n_flag_set(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x00)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_dec_n_flag_unset(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xC6)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x01)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEX

    def test_dex(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCA)

        self.execute()

        self.assertEqual(self.cpu_register('X'), 0x01)

    def test_dex_z_flag_set(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCA)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dex_z_flag_unset(self):
        self.cpu_set_register('X', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCA)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dex_n_flag_set(self):
        self.cpu_set_register('X', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCA)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_dex_n_flag_unset(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xCA)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // DEY

    def test_dey(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertEqual(self.cpu_register('Y'), 0x01)

    def test_dey_z_flag_set(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_dey_z_flag_unset(self):
        self.cpu_set_register('Y', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_dey_n_flag_set(self):
        self.cpu_set_register('Y', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_dey_n_flag_unset(self):
        self.cpu_set_register('Y', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x88)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ASL

    def test_asl_accumulator(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x04)

    def test_asl_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x06)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x04)

    def test_asl_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x16)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x04)

    def test_asl_absolute(self):

        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x0E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x04)

    def test_asl_absoluteX(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x1E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x04)

    def test_asl_c_flag_set(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_asl_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_asl_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_asl_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_asl_n_flag_set(self):
        self.cpu_set_register('A', 0xFE)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_asl_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x0A)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // LSR

    def test_lsr_accumulator(self):
        self.cpu_set_register('A', 0x2)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x01)

    def test_lsr_zeroPage(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x46)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x01)

    def test_lsr_zeropage_x(self):
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x56)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x01)

    def test_lsr_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x01)

    def test_lsr_absolute_x(self):
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x5E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x01)

    def test_lsr_c_flag_set(self):
        self.cpu_set_register('A', 0xFF)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_lsr_c_flag_unset(self):
        self.cpu_set_register('A', 0x10)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_lsr_z_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_lsr_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    # TODO: def test_lsr_n_flag_set(self): }
    # TODO: not tested, N bit always set to 0

    def test_lsr_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4A)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ROL

    def test_rol_accumulator(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x2)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x05)

    def test_rol_zeropage(self):

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x26)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x05)

    def test_rol_zeropage_x(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x36)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x05)

    def test_rol_absolute(self):

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x2E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x05)

    def test_rol_absolute_x(self):

        self.cpu_set_flag('C')
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x3E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x02)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x05)

    def test_rol_c_flag_set(self):
        self.cpu_set_register('A', 0x80)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_rol_c_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_rol_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_rol_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_rol_n_flag_set(self):
        self.cpu_set_register('A', 0xFE)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_rol_n_flag_unset(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x2A)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // ROR

    def test_ror_accumulator(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0x08)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertEqual(self.cpu_register('A'), 0x84)

    def test_ror_zeropage(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x66)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0084, 0x08)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x84)

    def test_ror_zeropage_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('X', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x76)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0085, 0x08)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x84)

    def test_ror_absolute(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x08)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0084), 0x84)

    def test_ror_absolute_x(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('X', 1)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x7E)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0085, 0x08)

        self.execute()

        self.assertEqual(self.memory_fetch(0x0085), 0x84)

    def test_ror_c_flag_set(self):
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    def test_ror_c_flag_unset(self):
        self.cpu_set_register('A', 0x10)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    def test_ror_z_flag_set(self):
        self.cpu_set_register('A', 0x00)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertTrue(self.cpu_flag('Z'))

    def test_ror_z_flag_unset(self):
        self.cpu_set_register('A', 0x02)
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertFalse(self.cpu_flag('Z'))

    def test_ror_n_flag_set(self):
        self.cpu_set_flag('C')
        self.cpu_set_register('A', 0xFE)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertTrue(self.cpu_flag('N'))

    def test_ror_n_flag_unset(self):
        self.cpu_unset_flag('C')
        self.cpu_set_register('A', 0x01)
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6A)

        self.execute()

        self.assertFalse(self.cpu_flag('N'))

    # // JMP

    def test_jmp_absolute(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x4C)
        self.memory_set(0x0101, 0xFF)
        self.memory_set(0x0102, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x01FF)

    def test_jmp_indirect(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x6C)
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x01)
        self.memory_set(0x0184, 0xFF)
        self.memory_set(0x0185, 0xFF)

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0xFFFF)

    # // JSR

    def test_jsr(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x20)
        self.memory_set(0x0101, 0xFF)
        self.memory_set(0x0102, 0x01)

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x01FF)
        self.assertEqual(self.memory_fetch(0x01FD), 0x01)
        self.assertEqual(self.memory_fetch(0x01FC), 0x02)

    def test_jsr_stack_pointer(self):
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x20)   # JSR
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0084, 0x60)   # RTS

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0084)
        self.assertEqual(self.cpu_register('SP'), 0xFB)

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0103)
        self.assertEqual(self.cpu_register('SP'), 0xFD)

    def test_jsr_with_illegal_opcode(self):
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x20)   # JSR $0084
        self.memory_set(0x0101, 0x84)
        self.memory_set(0x0102, 0x00)
        self.memory_set(0x0103, 0xA9)   # LDA #$ff
        self.memory_set(0x0104, 0xFF)
        self.memory_set(0x0105, 0x02)   # illegal opcode
        self.memory_set(0x0084, 0x60)   # RTS

        self.execute()   # JSR
        self.execute()   # LDA
        self.execute()   # illegal
        self.execute()   # RTS

        self.assertEqual(self.cpu_register('A'), 0xFF)

    # // RTS

    def test_rts(self):
        self.cpu_pc(0x0100)
        self.cpu_push_word(0x0102)
        self.memory_set(0x0100, 0x60)

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0103)

    # // BCC

    def test_bcc(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 2)
        self.assertEqual(self.cpu_register('PC'), 0x0102)

        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)
        self.memory_set(0x0101, 0x02)   # +2

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 3)
        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x90)
        self.memory_set(0x0101, 0xFD)   # -3

        cycles, _ = self.execute()

        if self.check_cycles():
            self.assertEqual(cycles, 4)
        self.assertEqual(self.cpu_register('PC'), 0x00FF)

    # // BCS

    def test_bcs(self):
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB0)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)
        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB0)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BEQ

    def test_beq(self):
        self.cpu_set_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF0)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF0)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BMI

    def test_bmi(self):
        self.cpu_set_flag('N')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x30)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('N')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x30)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BNE

    def test_bne(self):
        self.cpu_unset_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD0)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('Z')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD0)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BPL

    def test_bpl(self):

        self.cpu_unset_flag('N')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x10)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_unset_flag('N')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x10)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BVC

    def test_bvc(self):
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x50)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x50)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // BVS

    def test_bvs(self):
        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x70)
        self.memory_set(0x0101, 0x02)   # +2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0104)

        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x70)
        self.memory_set(0x0101, 0xFE)   # -2

        self.execute()

        self.assertEqual(self.cpu_register('PC'), 0x0100)

    # // CLC

    def test_clc(self):
        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x18)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0x18)

        self.execute()

        self.assertFalse(self.cpu_flag('C'))

    # // CLD

    def test_cld(self):
        self.cpu_unset_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xD8)

        self.execute()

        self.assertFalse(self.cpu_flag('D'))

        # TODO: review this
        self.cpu_set_flag('D')
        self.cpu_pc(0x0100)

        self.memory_set(0x0100, 0xD8)

        self.execute()
        # TODO: check if it wasn't true
        self.assertFalse(self.cpu_flag('D'))

    # // CLI

    def test_cli(self):
        self.cpu_unset_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x58)

        self.execute()

        self.assertFalse(self.cpu_flag('I'))

        self.cpu_set_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x58)

        self.execute()

        self.assertFalse(self.cpu_flag('I'))

    # // CLV

    def test_clv(self):
        self.cpu_unset_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB8)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

        self.cpu_set_flag('V')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xB8)

        self.execute()

        self.assertFalse(self.cpu_flag('V'))

    # // SEC

    def test_sec(self):
        self.cpu_unset_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x38)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

        self.cpu_set_flag('C')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x38)

        self.execute()

        self.assertTrue(self.cpu_flag('C'))

    # // SED

    def test_sed(self):
        self.cpu_unset_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF8)

        self.execute()

        self.assertTrue(self.cpu_flag('D'))

        self.cpu_set_flag('D')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0xF8)

        self.execute()

        self.assertTrue(self.cpu_flag('D'))

    # // SEI

    def test_sei(self):
        self.cpu_unset_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x78)

        self.execute()

        self.assertTrue(self.cpu_flag('I'))

        self.cpu_set_flag('I')
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x78)

        self.execute()

        self.assertTrue(self.cpu_flag('I'))

    # // BRK

    def test_brk(self):
        self.cpu_set_register('P', 0xFF - Status.B)  # Exclude B Flag
        self.cpu_pc(0x0100)
        self.memory_set(0x0100, 0x00)
        self.memory_set(0xFFFE, 0xFF)
        self.memory_set(0xFFFF, 0x01)

        self.execute()

        self.assertEqual(self.cpu_pull_byte(), 0xFF)
        self.assertEqual(self.cpu_pull_word(), 0x0102)
        self.assertEqual(self.cpu_register('PC'), 0x01FF)

    # // RTI

    def test_rti(self):
        self.cpu_pc(0x0100)
        self.cpu_push_word(0x0102)
        self.cpu_push_byte(0x03)
        self.memory_set(0x0100, 0x40)

        self.execute()

        # Overflow flag set seens odd
        # TODO: self.assertEqual(self.cpu_register('P'), 0x23)
        self.assertEqual(self.cpu_register('PC'), 0x0102)

    # // Rom

    # def test_Rom(self):

    #     cpu.DisableDecimalMode()

    #     self.cpu_set_register('P', 0x24)
    #     cpu.Registers.SP = 0xfd
    #     cpu.Registers.PC = 0xc000

    #     cpu.Memory.(*BasicMemory).load("test-roms/nestest/nestest.nes")

    #     self.memory_set(0x4004, 0xff)
    #     self.memory_set(0x4005, 0xff)
    #     self.memory_set(0x4006, 0xff)
    #     self.memory_set(0x4007, 0xff)
    #     self.memory_set(0x4015, 0xff)

    #     err := cpu.Run()

    #     if err != nil {
    #         switch err.(type) {
    #         case BrkOpCodeError:
    #         default:
    #             t.Error("Error during Run\n")
    #         }
    #     }

    #     self.assertEqual(self.memory_fetch(0x0002), 0x00)

    #     self.assertEqual(self.memory_fetch(0x0003), 0x00)

    # // Irq

    @skip('TODO')
    def test_irq_interrupt(self):
        self.cpu_set_register('P', 0xFB)
        self.cpu_pc(0x0100)

        self.cpu_force_interrupt('irq')

        self.memory_set(0xFFFE, 0x40)
        self.memory_set(0xFFFF, 0x01)

        self.execute_interrupt()

        self.assertEqual(self.cpu_pull_byte(), 0xFB)
        self.assertEqual(self.cpu_pull_word(), 0x0100)

        self.assertEqual(self.cpu_register('PC'), 0x0140)

        self.assertFalse(self.cpu_get_interrupt('irq'))

    # // Nmi

    @skip('TODO')
    def test_nmi_interrupt(self):
        self.cpu_set_register('P', 0xFF)
        self.cpu_pc(0x0100)

        self.cpu_force_interrupt('nmi')

        self.memory_set(0xFFFA, 0x40)
        self.memory_set(0xFFFB, 0x01)

        self.execute_interrupt()

        self.assertEqual(self.cpu_pull_byte(), 0xFF)
        self.assertEqual(self.cpu_pull_word(), 0x0100)

        self.assertEqual(self.cpu_register('PC'), 0x0140)

        self.assertFalse(self.cpu_get_interrupt('nmi'))

    # // Rst

    @skip('TODO')
    def test_rst_interrupt(self):

        self.cpu_pc(0x0100)
        self.cpu_force_interrupt('rst')
        self.memory_set(0xFFFC, 0x40)
        self.memory_set(0xFFFD, 0x01)

        self.cpu.execute_interrupt()

        self.assertEqual(self.cpu_register('PC'), 0x0140)

        self.assertFalse(self.cpu_get_interrupt('rst'))
