from ctci.chapter02 import linked_lists


def delete_middle_node(node: linked_lists.SinglyLinkedNode) -> linked_lists.SinglyLinkedNode:
    """
    Logically deletes the node by copying the data from the node it points to
    and deleting the node it points to. Returns the input after changing its
    data.

    Raises a ValueError if the node cannot be deleted without a reference to the
    previous node.
    """

    if node is None or node.next is None:
        raise ValueError("This node cannot delete itself")

    node.data = node.next.data
    node.next = node.next.next

    return node
