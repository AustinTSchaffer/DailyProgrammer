import functools

NUM_BITS = 32

class Solution:
    def reverseBits(self, n: int) -> int:
        output = 0
        for _ in range(NUM_BITS):
            output = (output << 1) | (n & 1)
            n = n >> 1
        return output

    # @param n, an integer
    # @return an integer
    def reverseBits2(self, n):
        ret, power = 0, 24
        while n:
            ret += self.reverseByte(n & 0xff) << power
            n = n >> 8
            power -= 8
        return ret

    # memoization with decorator
    @functools.lru_cache(maxsize=256)
    def reverseByte(self, byte):
        return (byte * 0x0202020202 & 0x010884422010) % 1023
