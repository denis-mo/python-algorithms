import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, m=42, k=3):
        self.bits = bitarray(m)
        self.bits.setall(0)
        self.k = k
        self.m = m

    def add(self, el):
        el_bits = self.__generate_bits(el)
        print(el_bits)
        for i in el_bits:
            self.bits[i] = 1

    def test(self, el):
        for i in self.__generate_bits(el):
            if not self.bits[i]:
                return False
        return True

    def __generate_bits(self, el):
        return [(mmh3.hash(el, i) % self.m) for i in range(self.k)]

