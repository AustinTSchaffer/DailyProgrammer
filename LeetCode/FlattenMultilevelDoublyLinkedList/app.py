from typing import Tuple

class _Node:
    def __init__(self,
                 val,
                 prev = None,
                 next = None,
                 child = None,
                 ):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


class Solution:
    def flatten(self, head: _Node) -> _Node:
        head, _ = flatten_and_return_tail(head)

        return head


def flatten_and_return_tail(head: _Node) -> Tuple[_Node, _Node]:
    if head is None:
        return None, None

    ORIG_HEAD = head
    curr_node = head

    while True:
        if curr_node.child is not None:
            prev_head_next = curr_node.next

            child_head, child_tail = flatten_and_return_tail(curr_node.child)
            curr_node.child = None

            curr_node.next = child_head
            child_head.prev = curr_node

            if prev_head_next is not None:
                prev_head_next.prev = child_tail
                child_tail.next = prev_head_next
                curr_node = prev_head_next
            else:
                return ORIG_HEAD, child_tail

        if curr_node.next is None:
            return ORIG_HEAD, curr_node

        curr_node = curr_node.next


def generate_branch(data: list) -> _Node:
    assert len(data) > 0

    head_node = _Node(data[0])
    prev_node = head_node

    for index in range(1, len(data)):
        curr_value = data[index]
        curr_node = _Node(curr_value, prev=prev_node)
        prev_node.next = curr_node
        prev_node = curr_node

    return head_node


def branch_to_list(head: _Node) -> list:
    output = []
    curr = head
    while curr is not None:
        output.append(curr.val)
        curr = curr.next
    return output
