class Solution:
    def hammingDistance(self, x: int, y: int) -> int:
        diff = 0

        while x or y:
            diff += 0 if ((x & 1) == (y & 1)) else 1
            x = x >> 1
            y = y >> 1

        return diff

if __name__ == '__main__':
    s = Solution()
    assert s.hammingDistance(1, 1) == 0
    assert s.hammingDistance(1, 2) == 2
    assert s.hammingDistance(1, 4) == 2
    assert s.hammingDistance(1, 0) == 1
