import unittest

import app

class TestApp(unittest.TestCase):
    solution = app.Solution()

    def test_tree_1(self):
        tree = _test_tree_1()
        result = self.solution.widthOfBinaryTree(tree)
        self.assertEqual(result, 4)

    def test_tree_2(self):
        tree = _test_tree_2()
        result = self.solution.widthOfBinaryTree(tree)
        self.assertEqual(result, 2)

    def test_tree_3(self):
        tree = _test_tree_3()
        result = self.solution.widthOfBinaryTree(tree)
        self.assertEqual(result, 2)

    def test_tree_4(self):
        tree = _test_tree_4()
        result = self.solution.widthOfBinaryTree(tree)
        self.assertEqual(result, 8)

def _test_tree_1() -> app._TreeNode:
    r"""
    Returns representation of tree:
         1
       /   \
      3     2
     / \     \
    5   3     9
    """
    return app._TreeNode(
        1,
        left=app._TreeNode(
            3,
            left=app._TreeNode(5),
            right=app._TreeNode(3),
        ),
        right=app._TreeNode(
            2,
            right=app._TreeNode(9),
        )
    )

def _test_tree_2() -> app._TreeNode:
    r"""
    Returns representation of tree:
          1
         /
        3
       / \
      5   3
    """
    return app._TreeNode(
        1,
        left=app._TreeNode(
            3,
            left=app._TreeNode(5),
            right=app._TreeNode(3),
        )
    )

def _test_tree_3() -> app._TreeNode:
    r"""
    Returns representation of tree:
          1
         / \
        3   2
       /
      5
    """
    return app._TreeNode(
        1,
        left=app._TreeNode(
            3,
            left=app._TreeNode(5)
        ),
        right=app._TreeNode(2),
    )

def _test_tree_4() -> app._TreeNode:
    r"""
    Returns representation of tree:
          1
         / \
        3   2
       /     \
      5       9
     /         \
    6           7
    """
    return app._TreeNode(
        1,
        left=app._TreeNode(3, left=app._TreeNode(5, left=app._TreeNode(6))),
        right=app._TreeNode(2, right=app._TreeNode(9, right=app._TreeNode(8))),
    )

if __name__ == '__main__':
    unittest.main()
