#!/usr/bin/env python3
"""
TASK: Implement all needed functions to execute unittests without errors.
Body of the function can contain only 1 line (usage of ';' is not allowed).
"""
import unittest
from functools import reduce


# INSERT YOUR CODE HERE


class TestTask8(unittest.TestCase):

    def test_1(self):
        arr = [1, 2, 3, 4, 5, 6]
        expected = [6, 5, 4, 3, 2, 1]
        self.assertListEqual(func1(arr), expected)

    def test_2(self):
        arr = [[1, 2], [3, 4], [5, 6, 7], [8], [9, 10]]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertListEqual(func2(arr), expected)

    def test_3(self):
        arr = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
        expected = [3, 7, 11, 15, 19]
        self.assertListEqual(func3(arr), expected)

    def test_4(self):
        arr = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
        expected = [15, 18, 21, 24]
        self.assertListEqual(func4(arr), expected)

    def test_5(self):
        arr = [7, 0, 6, -6, 90, -1, -12, 11, -8, 6, 6, 2, -5, 1]
        expected = [7, 6, 90, 11, 6, 6, 2, 1]
        self.assertListEqual(func5(arr), expected)

    def test_6(self):
        arr = ['a 3', 'f 9', 'e 98', 'd 1', 'u 5', 'h 2', 'p 0', 'r 18', 'q 11', 'v 17']
        expected = ['p 0', 'd 1', 'h 2', 'a 3', 'u 5', 'f 9', 'q 11', 'v 17', 'r 18', 'e 98']
        self.assertListEqual(func6(arr), expected)

    def test_7(self):
        arr = [[1, 0, 1], [1], [0, 1], [1, 1, 1, 1], [0, 0], [1, 1, 0], [1, 1]]
        expected = [False, True, False, True, False, False, True]
        self.assertListEqual(func7(arr), expected)

    def test_8(self):
        arr = [[7, 14, 2], [6], [67, 12], [-543, -643], [5, 2], [9, 26, -3], [12, 43, 65, 22], [-11, 17], [3, 1]]
        expected = [2, 6, 12, 0, 2, 0, 12, 0, 1]
        self.assertListEqual(func8(arr), expected)

    def test_9(self):
        arr = [1.5, 6.2, 4.8, 1.4, 2.93, 9.01, 5.3]
        expected = [4, 36, 25, 1, 9, 81, 25]
        self.assertListEqual(func9(arr), expected)

    def test_10(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected = ['0b10', '0b100', '0b110', '0b1000', '0b1010', '0b1100', '0b1110', '0b10000', '0b10010']
        self.assertListEqual(func10(arr), expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
