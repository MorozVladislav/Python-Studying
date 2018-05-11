#!/usr/bin/env python3
"""
TASK: Implement functions which use 'closure' with so much different ways as you can
to execute unittests without errors (put functions to the 'FUNC_FACTORIES' list).
"""
import functools
import operator
import unittest


def make_addition_1(x):
    def addition(y):
        return x + y
    return addition


def make_addition_2(x):
    return functools.partial(operator.add, x)


def make_addition_3(x):

    def addition_value(value):
        def wrapper(func):
            def wrapped(*args, **kwargs):
                return func(*args, **kwargs) + value
            return wrapped
        return wrapper

    @addition_value(x)
    def return_value(y):
        return y

    return return_value


def make_addition_4(x):
    return lambda y: x + y


class make_addition_5(object):
    def __init__(self, x):
        self.x = x

    def __call__(self, y):
        return self.x + y


FUNC_FACTORIES = [
    make_addition_1,
    make_addition_2,
    make_addition_3,
    make_addition_4,
    make_addition_5,
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
