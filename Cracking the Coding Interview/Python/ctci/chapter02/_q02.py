from ctci.chapter02 import linked_lists


def kth_element(l_list: linked_lists.SinglyLinkedList, k: int) -> linked_lists.SinglyLinkedNode:
    """

    Returns the kth element from the input linked list.

    """

    for i, node in enumerate(l_list):
        if i == k:
            return node

    raise ValueError("k is out of range for l_list")


def kth_to_last_element(l_list: linked_lists.SinglyLinkedList, k: int) -> linked_lists.SinglyLinkedNode:
    """

    Returns the kth-to-last element from the input linked list.

    This is a trivial solution which first calculates the length of the list,
    then calculates the index of the kth-to-last element, reusing the
    functionality of `kth_element`.

    This solution has constant space complexity and `O(2n)` time complexity.

    """

    length = 0
    for _ in l_list:
        length += 1

    if k >= length:
        raise ValueError("k is out of range for l_list")

    return kth_element(l_list, length - k - 1)


def kth_to_last_element2(l_list: linked_lists.SinglyLinkedList, k: int) -> linked_lists.SinglyLinkedNode:
    """

    Returns the kth-to-last element from the input linked list.

    This is a recursive solution which recursively iterates through the list
    forwards, then counts from 0 as it iterates through the list backwards,
    until k matches the count, returning that element.

    This solution has `O(n)` space complexity and `O(2n)` time complexity.

    """

    def _rec(node: linked_lists.SinglyLinkedNode):
        if node is None:
            return 0

        result = _rec(node.next)

        if type(result) is linked_lists.SinglyLinkedNode:
            return result

        if result == k:
            return node

        return result + 1

    result = _rec(l_list.head)

    if type(result) is linked_lists.SinglyLinkedNode:
        return result

    raise ValueError("k is out of range for l_list")
