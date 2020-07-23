import collections
from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        num_freq = collections.defaultdict(int)
        for num in nums:
            num_freq[num] += 1
        return [ num for num in num_freq if num_freq[num] == 1 ]

    def singleNumberUsingCounter(self, nums: List[int]) -> List[int]:
        num_freq = collections.Counter(nums)
        return [ num for num in num_freq if num_freq[num] == 1 ]
