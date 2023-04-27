import math

from ctci.chapter02 import linked_lists


def to_little_endian_int(l_list: linked_lists.SinglyLinkedList) -> int:
    """

    Returns a little-endian integer representation of the linked list. The list
    must contain integer data, with all values being between 0 and 9,
    inclusively.

    Example: `[1 -> 2 -> 3]` -> `321`

    """

    cu_sum = 0
    digit = 0

    for node in l_list:
        assert type(node.data) is int and node.data < 10 and node.data >= 0

        cu_sum += node.data * math.pow(10, digit)
        digit += 1

    return int(cu_sum)


def from_little_endian_int(value: int) -> linked_lists.SinglyLinkedList:
    """

    Returns a linked list from a little-endian integer representation of a linked
    list.

    Example: `123` -> `[3 -> 2 -> 1]`

    """
    assert value >= 0

    l_list = linked_lists.SinglyLinkedList()

    if value == 0:
        l_list.append(0)
        return l_list

    while value != 0:
        l_list.append(value % 10)
        value = value // 10

    return l_list


def to_big_endian_int(l_list: linked_lists.SinglyLinkedList) -> int:
    """

    Returns a big-endian integer representation of the linked list. The list
    must contain integer data, with all values being between 0 and 9,
    inclusively.

    Example: `[1 -> 2 -> 3]` -> `123`

    """

    formatted_number = ""

    for node in l_list:
        assert type(node.data) is int and node.data < 10 and node.data >= 0
        formatted_number += str(node.data)

    return int(formatted_number)


def from_big_endian_int(value: int) -> linked_lists.SinglyLinkedList:
    """

    Returns a linked list from a big-endian integer representation of a linked
    list.

    Example: `123` -> `[1 -> 2 -> 3]`

    """

    assert value >= 0

    l_list = linked_lists.SinglyLinkedList()

    for digit in str(value):
        l_list.append(int(digit))

    return l_list


def add_little_endian(*lists):
    """

    Adds together an arbitrary number of `linked_lists.SinglyLinkedList`
    instances, assuming that the lists contain only single integer, base-10
    digits, describing larger integers using little-endian. Returns a new
    instance of a `linked_lists.SinglyLinkedList`, also using little-endian.

    Example::

        [1 -> 2 -> 3] + [4 -> 5 -> 6]
        = 321 + 654
        = 975
        = [5 -> 7 -> 9]
    """
    return from_little_endian_int(sum(map(to_little_endian_int, lists)))


def add_big_endian(*lists):
    """

    Adds together an arbitrary number of `linked_lists.SinglyLinkedList`
    instances, assuming that the lists contain only single integer, base-10
    digits, describing larger integers using big-endian. Returns a new instance
    of a `linked_lists.SinglyLinkedList`, also using big-endian.

    Example::

        [1 -> 2 -> 3] + [4 -> 5 -> 6]
        = 123 + 456
        = 579
        = [5 -> 7 -> 9]
    """
    return from_big_endian_int(sum(map(to_big_endian_int, lists)))
