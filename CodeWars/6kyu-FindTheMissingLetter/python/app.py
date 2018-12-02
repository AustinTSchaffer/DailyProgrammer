from typing import Union
import string


def configurable_find_missing_letter(alphabet: str, chars: Union[str, list]) -> str:
    assert chars

    offset = alphabet.index(chars[0])

    for i,c in enumerate(chars[1:]):
        next_letter = alphabet[i + offset + 1]
        if c != next_letter:
            return next_letter

    raise "No letters are missing"


def find_missing_letter(chars: Union[str, list]) -> str:
    return configurable_find_missing_letter(string.ascii_letters, chars)
