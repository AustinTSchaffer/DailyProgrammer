from typing import List

# Definition for a binary tree node.
class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> _TreeNode:
        if not postorder: return None

        def _buildTree(inorder: list, postorder: list, root: _TreeNode):
            root.val = postorder[-1]
            val_index_inorder = inorder.index(root.val)

            if val_index_inorder > 0:
                # Perform slicing based on pivot
                left_inorder = inorder[:val_index_inorder]
                left_postorder = postorder[:val_index_inorder]

                # Create an empty instance of a tree node
                left_node = _TreeNode()
                root.left = left_node

                # Recurse
                _buildTree(left_inorder, left_postorder, left_node)

            if val_index_inorder + 1 < len(inorder):
                # Perform slicing based on pivot
                right_inorder = inorder[val_index_inorder+1:]
                right_postorder = postorder[val_index_inorder:-1]

                # Create an empty instance of a tree node
                right_node = _TreeNode()
                root.right = right_node

                _buildTree(right_inorder, right_postorder, right_node)


        tree = _TreeNode()
        _buildTree(inorder, postorder, tree)
        return tree

def calc_inorder(root: _TreeNode) -> list:
    def _inorder(root: _TreeNode, accumulator: list):
        if root is None:
            return

        _inorder(root.left, accumulator)
        accumulator.append(root.val)
        _inorder(root.right, accumulator)

    accumulator = []
    _inorder(root, accumulator)
    return accumulator


def calc_postorder(root: _TreeNode) -> list:
    if not root:
        return []

    def _postorder(root: _TreeNode, accumulator: list) -> list:
        if root is None:
            return

        _postorder(root.left, accumulator)
        _postorder(root.right, accumulator)
        accumulator.append(root.val)

    accumulator = []
    _postorder(root, accumulator)
    return accumulator
