from abc import abstractmethod, ABCMeta


class CPU6502Bridge(metaclass=ABCMeta):
    @abstractmethod
    def cpu_pc(self, counter):
        pass

    @abstractmethod
    def memory_set(self, pos, val):
        pass

    @abstractmethod
    def memory_fetch(self, pos):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def cpu_set_register(self, register, value):
        pass

    @abstractmethod
    def cpu_register(self, register):
        pass

    @abstractmethod
    def cpu_flag(self, flag):
        pass

    @abstractmethod
    def cpu_set_flag(self, flag):
        pass

    @abstractmethod
    def cpu_unset_flag(self, flag):
        pass

    @abstractmethod
    def cpu_push_byte(self, byte):
        pass

    @abstractmethod
    def cpu_pull_byte(self):
        pass

    @abstractmethod
    def cpu_push_word(self, word):
        pass

    @abstractmethod
    def cpu_pull_word(self):
        pass
