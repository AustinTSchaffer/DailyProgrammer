import json
import os
import functools

import num2words

_dir = os.path.dirname(os.path.realpath(__file__))
NUMBER_LABELS = json.load(open(_dir + "/number_labels.json"))

def number_label(label_number: int) -> str:
    """
    Returns the label for the specified "group of 3"

    TODO: Clarify language. What is a label? How can you visualize it?
    - http://mrob.com/pub/math/largenum.html#chuquet
    - http://mrob.com/pub/math/ln-notes1-2.html#adhoc_chuquet
    - http://mrob.com/pub/math/ln-notes1-2.html#chuquet_origins
    """

    if label_number == 0:
        return ""

    if label_number == 1:
        return "thousand"

    _result = label_number - 1
    output = ""
    while _result:
        remainder = _result % 1000
        output = NUMBER_LABELS[remainder] + output
        _result = _result // 1000

    return output + "on"

@functools.lru_cache(maxsize=1000)
def triple_name(triple_value: int) -> str:
    assert triple_value > 0 and triple_value <= 999, \
        "Only supports values between 1 and 999."

    return num2words.num2words(triple_value).replace(" and ", " ")
