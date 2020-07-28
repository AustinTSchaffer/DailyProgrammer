from typing import List
import collections

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        histogram = collections.Counter(tasks)
        sorted_histogram = histogram.most_common()
        _, max_num_occ = sorted_histogram[0]
        num_shared_occ = 0
        for _, num_occ in sorted_histogram:
            if num_occ != max_num_occ:
                break
            num_shared_occ += 1

        return max(
            (max_num_occ + ((max_num_occ-1) * n)) + (num_shared_occ - 1),
            len(tasks),
        )
