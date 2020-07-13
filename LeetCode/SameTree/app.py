# Definition for a binary tree node.
class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: _TreeNode, q: _TreeNode) -> bool:
        # If both are none, the nodes are the same.
        if p is None and q is None:
            return True

        # If either is none, one is not.
        if p is None or q is None:
            return False

        # No need to recurse if they're the same object.
        if id(p) == id(q):
            return True

        # Check the values and recurse, DFS.
        return (
            p.val == q.val
            and self.isSameTree(p.left, q.left)
            and self.isSameTree(p.right, q.right)
        )
