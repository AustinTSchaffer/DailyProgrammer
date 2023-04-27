from ctci.chapter02 import linked_lists

def get_loop_element(l_list: linked_lists.SinglyLinkedList) -> linked_lists.SinglyLinkedNode:
    """

    Returns a node from the list if the list contains a cycle, where an element
    at the "end" of the linked list has a `next` that refers to an element that
    exists earlier in the linked list. Returns the node at the "beginning" of
    the loop, which is the node that is referenced by the `next` property of 2
    different nodes within the input list. Returns None if the list contains no
    cycles.

    This is a naive solution with poor space and time complexity, with O(n)
    space complexity and O(n^2) time complexity.
    """

    prev_nodes = []
    for node in l_list:
        l_list.append(node)
        if node.next in prev_nodes:
            return node.next

    return None
