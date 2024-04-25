# from unittest import TestCase
# from wednesday.tests.mapper_spec import MapperSpec


# class MapperMMC1Test(MapperSpec, TestCase):

#     def given_mapper(self, ines_number):
#         raise NotImplementedError()

#     def given_pgr_banks(self, index, size):
#         raise NotImplementedError()

#     def given_chr_banks(self, index, size):
#         raise NotImplementedError()

#     def test_mapper_with_one_bank_mirrors_address_8000_and_C000(self):
#         self.given_mapper(1)
#         self.given_pgr_banks(1, '16k')
#         self.given_chr_banks(1, '4k')

#         self.set_pgr_bank_memory(1, 0, 0xFF)

#         self.assertEqual(self.fetch_bus_memory(0x8000), 0xff)
#         self.assertEqual(self.fetch_bus_memory(0xC000), 0xff)

#     def test_mapper_shift_register(self):
#         self.given_mapper(1)
#         self.given_pgr_banks(3)

#         self.set_pgr_bank(1, 0x00, 0x01)
#         self.set_pgr_bank(2, 0x00, 0x01)
#         self.set_pgr_bank(3, 0x00, 0x03)


#         # self.set_execute

#         self.assertEqual(self.fetch_bus_memory(0x8000), 0xff)
#         self.assertEqual(self.fetch_bus_memory(0x8000), 0xff)
#         self.assertEqual(self.fetch_bus_memory(0xC000), 0xff)

#     def test_reset_mapper(self):
#         self.given_mapper(1)
#         self.given_pgr_banks(3)

#         with self.compile_at(0xC000) as comp:
#             opcodes, table = comp(
#                 """
#                 resetMapper:
#                 lda #$80
#                 sta $8000
#                 rts
#                 """
#             )
