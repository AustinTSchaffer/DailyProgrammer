import unittest

import app

class Tests(unittest.TestCase):
    s = app.Solution()

    def test_reverse_bits_1(self):
        assert Tests.s.reverseBits(43261596) == 964176192
        assert Tests.s.reverseBits(964176192) == 43261596

    def test_reverse_bits_2(self):
        assert Tests.s.reverseBits(4294967293) == 3221225471
        assert Tests.s.reverseBits(3221225471) == 4294967293
