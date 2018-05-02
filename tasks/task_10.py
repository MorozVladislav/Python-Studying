#!/usr/bin/env python3
"""
TASK: Implement functions which use 'closure' with so much different ways as you can
to execute unittests without errors (put functions to the 'FUNC_FACTORIES' list).
"""
import functools
import operator
import unittest


# INSERT YOUR CODE HERE


FUNC_FACTORIES = [
]


class TestTask10(unittest.TestCase):

    def test_1(self):

        x, y = 20, 22
        functions = [func_factory(x) for func_factory in FUNC_FACTORIES]

        for func_add in functions:
            result = func_add(y)
            self.assertEqual(result, x + y)


if __name__ == '__main__':
    unittest.main(verbosity=2)
