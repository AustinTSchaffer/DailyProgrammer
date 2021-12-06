import os
from typing import List, Callable, TypeVar

T = TypeVar("T")

def get_input(script_dunder_file: str, filename="input.txt", callback: Callable[str, T]=None) -> List[T]:
    dir_ = os.path.dirname(script_dunder_file)
    with open(os.path.join(dir_, filename)) as input_:
        if callback:
            return list(map(callback, input_))
        return list(input_)
