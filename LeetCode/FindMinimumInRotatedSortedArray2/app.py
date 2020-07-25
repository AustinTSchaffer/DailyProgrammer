from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        first = nums[0]

        # Iterate until the next number is less than current.
        for num in nums:
            if num < first:
                return num

        return first
