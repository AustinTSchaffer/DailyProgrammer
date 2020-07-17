import unittest

import app


class Tests(unittest.TestCase):
    solution = app.Solution()

    def test_1(self):
        output = self.solution.topKFrequent(nums=[1, 1, 1, 2, 2, 3], k=2)
        assert len(output) == 2
        assert 1 in output
        assert 2 in output

    def test_2(self):
        output = self.solution.topKFrequent(nums=[1], k=1)
        assert output == [1]

    def test_3(self):
        nums = ([1, 2, 3] * 5000) + [4, 12, 3, 3, 4, 1, 1, 2]
        k = 2
        output = self.solution.topKFrequent(nums=nums, k=k)
        assert len(output) == 2
        assert 1 in output
        assert 3 in output

    def test_4(self):
        nums = [4, 12, 3, 3, 4, 1, 1, 2] + ([1, 2, 3] * 5000)
        k = 2
        output = self.solution.topKFrequent(nums=nums, k=k)
        assert len(output) == 2
        assert 1 in output
        assert 3 in output

    def test_5(self):
        nums = [4, 1, -1, 2, -1, 2, 3]
        k = 2
        output = self.solution.topKFrequent(nums=nums, k=k)
        assert len(output) == 2
        assert -1 in output
        assert 2 in output

    def test_6(self):
        nums = [5,2,5,3,5,3,1,1,3]
        k = 2
        output = self.solution.topKFrequent(nums=nums, k=k)
        assert len(output) == 2
        assert 5 in output
        assert 3 in output
