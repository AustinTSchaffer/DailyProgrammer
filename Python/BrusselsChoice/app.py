from dataclasses import dataclass
from typing import List, Tuple, Optional
from collections import namedtuple
import math

OPERATIONS = (
    2,
    0.5,
)

@dataclass
class Connection:
    value: int
    transformation: dict
    new_value: int


def get_neighbors(value: int) -> List[Connection]:
    """
    Returns a list of all of the neighbors of the value, each including a dict describing the transformation:

        sample_transformation = {
            "start": int,
            "end": int,
            "operation": float,
        }

    The `operation` describes the factor to multiply against the substring of `value`, specified by `start` and `end`.
    """

    str_value = str(value)

    return [
        result
        for end in range(len(str_value) + 1)
        for start in range(end)
        for operation in OPERATIONS
        if (result := apply_transformation(value, start=start, end=end, operation=operation))
    ]


def apply_transformation(value: int, *, start:int, end: int, operation: float) -> Optional[Connection]:
    # Substring must have a non-zero length
    if start == end:
        return None

    str_value = str(value)
    substring = int(str_value[start:end])

    # Substring must be even if dividing it by 2
    if (substring % 2 == 0) or float(operation).is_integer():
        return Connection(
            value=value,
            new_value=int(str_value[:start] + str(int(substring * operation)) + str_value[end:]),
            transformation={
                "start": start,
                "end": end,
                "operation": operation,
            },
        )

    return None

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_neighbors(2112))
