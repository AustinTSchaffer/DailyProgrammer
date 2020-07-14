import unittest

import app

class Tests(unittest.TestCase):
    solution = app.Solution()
    cases = [
        (12, 30, 165),
        (3, 30, 75),
        (3, 15, 7.5),
        (4, 50, 155),
        (12, 0, 0),
    ]

    def test_cases(self):
        for case in self.cases:
            self.assertAlmostEqual(
                first=self.solution.angleClock(
                    hour=case[0],
                    minutes=case[1],
                ),
                second=case[2],
                delta=pow(10, -5),
            )
