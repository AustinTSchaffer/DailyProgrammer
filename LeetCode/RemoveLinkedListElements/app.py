# Definition for singly-linked list.
class _ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeElements(self, head: _ListNode, val: int) -> _ListNode:
        prev = None
        curr = head

        while curr is not None:
            if curr.val == val:
                if prev is None:
                    head = curr.next
                    curr = head
                else:
                    prev.next = curr.next
                    curr = curr.next
            else:
                prev = curr
                curr = curr.next

        return head
