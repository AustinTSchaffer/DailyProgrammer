
from itertools import permutations
from typing import Tuple, Union, Optional
import dataclasses

@dataclasses.dataclass()
class SnailNumber:
    parent: Optional['SnailNumber']
    left: Union['SnailNumber', int]
    right: Union['SnailNumber', int]

    @classmethod
    def from_tuple(cls, parent, number):
        left, right = number

        self = cls(parent, None, None)
        self.left = left if isinstance(left, int) else cls.from_tuple(self, left)
        self.right = right if isinstance(right, int) else cls.from_tuple(self, right)

        return self

    @classmethod
    def from_snailnumber(cls, parent, snailnumber):
        left, right = snailnumber.left, snailnumber.right

        self = cls(parent, None, None)
        self.left = left if isinstance(left, int) else cls.from_snailnumber(self, left)
        self.right = right if isinstance(right, int) else cls.from_snailnumber(self, right)

        return self

    @classmethod
    def add(cls, left: 'SnailNumber', right: 'SnailNumber') -> 'SnailNumber':
        if left.parent is not None or right.parent is not None:
            raise ValueError('Cannot add subtrees.')

        self = cls(None, None, None)
        self.left = cls.from_snailnumber(self, left)
        self.right = cls.from_snailnumber(self, right)
        self.reduce()

        return self

    def __repr__(self):
        return f'[{self.left}, {self.right}]'

    def reduce(self):
        while self.explode() or self.split(): ...

    def explode(self) -> bool:
        def _explode(sn: SnailNumber, depth: int) -> bool:
            if depth == 4:
                if not isinstance(sn.right, int) or not isinstance(sn.right, int):
                    raise ValueError(f"This ~tree~ Snail Number is too deep. Should never have an SN with depth 5. {self}")

                # Find next number to the right and increment it by sn.right
                current = sn
                while (parent := current.parent) is not None:
                    if id(current) != id(parent.right):
                        if isinstance(parent.right, int):
                            parent.right += sn.right
                            break

                        parent = parent.right
                        # parent now points to a subtree that we need to explore
                        while not isinstance(parent.left, int):
                            parent = parent.left

                        parent.left += sn.right
                        break
                    
                    current = parent

                # Find next number to the left and increment it by sn.left
                current = sn
                while (parent := current.parent) is not None:
                    if id(current) != id(parent.left):
                        if isinstance(parent.left, int):
                            parent.left += sn.left
                            break

                        parent = parent.left
                        # parent now points to a subtree that we need to explore
                        while not isinstance(parent.right, int):
                            parent = parent.right

                        parent.right += sn.left
                        break
                    
                    current = parent

                # Clear the pointer to the snail number currently identified as "sn"
                if id(sn.parent.left) == id(sn):
                    sn.parent.left = 0
                else:
                    sn.parent.right = 0

                # Report that this number exploded.
                return True

            elif isinstance(sn.left, SnailNumber) and _explode(sn.left, depth+1):
                return True

            elif isinstance(sn.right, SnailNumber) and _explode(sn.right, depth+1):
                return True

            return False

        return _explode(self, 0)

    def split(self) -> bool:
        def _calc_split(num: int):
            return (num // 2), ((num // 2) + (num % 2))

        if isinstance(self.left, int):
            if self.left > 9:
                self.left = SnailNumber(self, *_calc_split(self.left))
                return True
        elif self.left.split():
            return True

        if isinstance(self.right, int):
            if self.right > 9:
                self.right = SnailNumber(self, *_calc_split(self.right))
                return True
        elif self.right.split():
            return True

        return False

    @property
    def magnitude(self) -> int:
        return (
            (3 * (self.left if isinstance(self.left, int) else self.left.magnitude)) +
            (2 * (self.right if isinstance(self.right, int) else self.right.magnitude))
        )

from common import get_input

if __name__ == '__main__':
    import functools
    snail_numbers = get_input(__file__, lambda line: SnailNumber.from_tuple(None, eval(line)))
    addition_result = functools.reduce(SnailNumber.add, snail_numbers)
    print('Part 1:', addition_result.magnitude)

    import itertools

    x = max(
        functools.reduce(SnailNumber.add, pair).magnitude
        for pair in itertools.permutations(snail_numbers, 2)
    )
    print('Part 2:', x)
