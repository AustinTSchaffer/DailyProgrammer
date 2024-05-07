import unittest

import fib

class TestFibonacci(unittest.TestCase):
    def test_base_case_0(self):
        self.assertEqual(fib.fib_iter(0), 0)

    def test_base_case_1(self):
        self.assertEqual(fib.fib_iter(1), 1)

    def test_case_2(self):
        self.assertEqual(fib.fib_iter(2), 1)

    def test_case_6(self):
        self.assertEqual(fib.fib_iter(6), 8)

    def test_negatives_throw_error(self):
        ...
    
    def test_non_integer_throw_error(self):
        ...

    

if __name__ == '__main__':
    unittest.main()
