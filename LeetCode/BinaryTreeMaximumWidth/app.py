from typing import Iterable, List, Tuple

class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def widthOfBinaryTree(self, root: _TreeNode) -> int:
        return max(
            level_width(level)
            for level in
            iter_levels(root)
        )

def iter_levels(root: _TreeNode) -> Iterable[List[Tuple[_TreeNode, int]]]:
    # Keeps track of the previous level in the tree, keeping track of a pointer
    # to the tree node as well as the position of that node within that level.
    previous_level = [(root, 1)]

    while any(previous_level):
        yield previous_level
        next_level = []

        for tree_node, position in previous_level:
            # Since the previous-level list keeps track of the position of
            # each node within the level in the tree, any None nodes can
            # be thrown out. The positions of nodes in their level in the
            # tree are equal to either 2x-1 or 2x the position of their parent
            # node:
            #         1
            #       /   \
            #      1     2
            #     / \   / \
            #    1   2 3   4
            if tree_node is not None:
                if tree_node.left is not None:
                    next_level.append((
                        tree_node.left,
                        (position * 2) - 1
                    ))

                if tree_node.right is not None:
                    next_level.append((
                        tree_node.right,
                        (position * 2)
                    ))

        previous_level = next_level

def level_width(level: List[Tuple[_TreeNode, int]]) -> int:
    left_index = level[0][1]
    right_index = level[-1][1]

    return right_index - left_index + 1
