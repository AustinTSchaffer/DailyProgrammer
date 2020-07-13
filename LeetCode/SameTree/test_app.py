import unittest

import app

class Tests(unittest.TestCase):
    s = app.Solution()

    def test_tree_eq_self(self):
        tree = app._TreeNode(1, left=app._TreeNode(2), right=app._TreeNode(3))

        assert self.s.isSameTree(None, None)
        assert self.s.isSameTree(tree, tree)

    def test_example_1(self):
        tree_1 = app._TreeNode(1, left=app._TreeNode(2), right=app._TreeNode(3))
        tree_2 = app._TreeNode(1, left=app._TreeNode(2), right=app._TreeNode(3))

        assert self.s.isSameTree(tree_1, tree_2)

    def test_example_2(self):
        tree_1 = app._TreeNode(1, left=app._TreeNode(2))
        tree_2 = app._TreeNode(1, right=app._TreeNode(2))

        assert not self.s.isSameTree(tree_1, tree_2)

    def test_example_3(self):
        tree_1 = app._TreeNode(1, left=app._TreeNode(2), right=app._TreeNode(1))
        tree_2 = app._TreeNode(1, left=app._TreeNode(1), right=app._TreeNode(2))

        assert not self.s.isSameTree(tree_1, tree_2)
