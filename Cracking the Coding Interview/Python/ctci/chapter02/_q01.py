from ctci.chapter02 import linked_lists


def remove_duplicates(l_list: linked_lists.SinglyLinkedList) -> linked_lists.SinglyLinkedList:
    """
    Removes duplicates from the linked list by keeping a set of the values.
    """

    values = set()
    for node in l_list:
        if node.data in values:
            l_list.delete(node.data)
        values.add(node.data)
    return l_list


def remove_duplicates2(l_list: linked_lists.SinglyLinkedList) -> linked_lists.SinglyLinkedList:
    """
    Removes duplicates from the linked list without keeping a set of the values.
    """

    for node in l_list:
        for runner in l_list:
            if runner == node:
                break
            if node.data == runner.data:
                l_list.remove(runner)
                break

    return l_list
