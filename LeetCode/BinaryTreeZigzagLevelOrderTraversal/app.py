from typing import List

# Definition for a binary tree node.
class _TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def zigzagLevelOrder(self, root: _TreeNode) -> List[List[int]]:
        direction = -1

        current_row = [root]
        output = []

        while current_row:
            next_row = []
            output_row = []

            for index in range(len(current_row) - 1, -1, -1):
                node = current_row[index]
                if not node:
                    continue

                output_row.append(node.val)

                if direction < 0:
                    if node.left:
                        next_row.append(node.left)
                    if node.right:
                        next_row.append(node.right)
                else:
                    if node.right:
                        next_row.append(node.right)
                    if node.left:
                        next_row.append(node.left)

            if output_row:
                output.append(output_row)

            current_row = next_row
            direction *= -1

        return output
