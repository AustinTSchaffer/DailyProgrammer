from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        power_sets = []

        for power_set in range(pow(2, len(nums))):
            current_set = []
            power_sets.append(current_set)

            index = 0
            while power_set != 0:
                if power_set & 1:
                    current_set.append(nums[index])

                power_set = power_set >> 1
                index += 1

        return power_sets
