from typing import List, Set, Tuple, Iterable
import unittest
from collections import defaultdict

TARGET = 0


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums = cleanup_nums(3, nums)

        results_set = set()
        results = []

        for index, value in enumerate(nums):
            for two_sum_result in two_sum(TARGET - value, nums, index + 1):
                # Create a tuple from pinned value and sub-result. The values
                # in this tuple will be ordered due to the list of nums being
                # ordered and the outputs of `two_sum` being ordered.
                result = (value, *two_sum_result)

                # Make sure the current result is distinct.
                if result in results_set:
                    continue

                # Record the result in output format and "O(1) lookup" format
                results_set.add(result)
                results.append(list(result))

        return results


def two_sum(target: int, nums: List[int], start_index=0) -> Iterable[Tuple[int]]:
    # Keeps track of the values in nums seen so far
    previous_values = set()

    # Since this implementation is meant to help three_sum, this implementation
    # of two_sum allows you to omit a leading range of indexes.
    for index in range(start_index, len(nums)):
        current_value = nums[index]

        # Check to see if a value that equals the diff between the target and
        # the current value has already been seen. If so, yield it as a result.
        diff = (target - current_value)
        if diff in previous_values:
            # Returned in this order to preserve input order, which should be sorted.
            yield (diff, current_value)

        # This value has now been seen before.
        previous_values.add(current_value)


def cleanup_nums(max_each_num: int, nums: List[int]) -> List[int]:
    """
    Sorts the input list of numbers making sure that each number only appears
    at most `max_each_num` times in the output.
    """

    histogram = defaultdict(int)

    for num in nums:
        histogram[num] += 1

    return [
        number
        for number in sorted(histogram.keys())
        for _ in range(min(max_each_num, histogram[number]))
    ]


class Tests(unittest.TestCase):
    def test_1(self):
        _input = [-1, 0, -1, 1, 2, -4]
        _output = [
            [-1, 0, 1],
            [-1, -1, 2],
        ]

        solution = Solution()
        self.assertListEqual(solution.threeSum(_input), _output)

    def test_2(self):
        _input = [1, 0, -1] * 1000000
        _output = [
            [-1, 0, 1],
            [0, 0, 0],
        ]

        solution = Solution()
        self.assertListEqual(solution.threeSum(_input), _output)

