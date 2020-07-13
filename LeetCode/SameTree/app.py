# Definition for a binary tree node.
class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: _TreeNode, q: _TreeNode) -> bool:
        if p is None and q is None:
            # If both are none, the nodes are the same.
            return True

        if p is None or q is None:
            # If either is none, one is not.
            return False

        if id(p) == id(q):
            # No need to recurse if they're the same object.
            return True

        # Check the values and recurse symmetrically, DFS.
        return (
            p.val == q.val
            and self.isSameTree(p.left, q.left)
            and self.isSameTree(p.right, q.right)
        )
