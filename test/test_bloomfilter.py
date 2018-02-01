import unittest

from bloomfilter import BloomFilter


class TestBloomFilter(unittest.TestCase):
    def test_contains(self):
        bf = BloomFilter()
        bf.add('t1')
        bf.add('t2')

        self.assertTrue(bf.test("t2"))

    def test_excluded(self):
        bf = BloomFilter()
        bf.add('t1')
        bf.add('t2')

        test1 = bf.test("t3")
        test2 = bf.test("t4")
        test3 = bf.test("t5")
        # making few checks to eliminate test failings on false positives
        self.assertFalse(test1 and test2 and test3)
