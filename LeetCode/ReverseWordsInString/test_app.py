import unittest

import app

class Tests(unittest.TestCase):
    solution = app.Solution()

    def test_example_1(self):
        self.assertEqual(
            self.solution.reverseWords("the sky is blue"),
            "blue is sky the"
        )

    def test_example_2(self):
        self.assertEqual(
            self.solution.reverseWords("  hello world!  "),
            "world! hello"
        )
    
    def test_example_3(self):
        self.assertEqual(
            self.solution.reverseWords("a good   example"),
            "example good a"
        )
