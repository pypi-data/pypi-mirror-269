# from unittest import TestCase
# from wednesday.tests.mapper_spec import MapperSpec


# class Mapper0NROMTest(MapperSpec, TestCase):

#     def given_mapper(self, ines_number):
#         raise NotImplementedError()

#     def given_pgr_banks(self, index, size):
#         raise NotImplementedError()

#     def given_chr_banks(self, index, size):
#         raise NotImplementedError()

#     def test_mapper_mirrors_address_8000_and_C000(self):
#         self.given_mapper(1)
#         self.given_pgr_banks(1, '16k')
#         self.given_chr_banks(1, '4k')

#         self.set_pgr_bank_memory(1, 0, 0xFF)

#         self.assertEqual(self.fetch_bus_memory(0x8000), 0xff)
#         self.assertEqual(self.fetch_bus_memory(0xC000), 0xff)

#     def test_mapper_mirror_execute(self):
#         self.given_mapper(1)
#         self.given_pgr_banks(1, '16k')
#         self.given_chr_banks(1, '4k')

#         with self.compile_at(bank=1, addr=0x8000) as comp:
#             comp(
#                 """
#                 ldx $8000
#                 ldy $C000
#                 """
#             )

#         self.execute()
#         self.execute()
