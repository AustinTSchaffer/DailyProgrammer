from typing import List

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        histogram = {}

        for num in nums:
            if num in histogram:
                histogram[num] += 1
            else:
                histogram[num] = 1

        output = [
            item[0] for item in
            sorted(
                histogram.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:k]
        ]

        return output
