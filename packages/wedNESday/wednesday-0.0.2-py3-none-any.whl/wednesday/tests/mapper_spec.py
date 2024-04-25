class INESCartridge:
    def __init__(self) -> None:
        self._pgr_rom = 0
        self._chr_rom = 0
        self._flag_6 = 0
        self._flag_7 = 0
        self._flag_8 = 0
        self._flag_9 = 0
        self._flag_10 = 0


class MapperSpec:
    def given_mapper(self, ines_number):
        raise NotImplementedError()

    def given_pgr_banks(self, index, size):
        raise NotImplementedError()

    def given_chr_banks(self, index, size):
        raise NotImplementedError()
