#!/usr/bin/env python3
"""
TASK: Implement at least functions 'test1_func1', 'test2_func1', 'test3_func1', 'test3_func2'
to execute unittests without errors.
"""
import functools
import random
import time
import types
import unittest

MY_DICT = {
    'a': [1, 2, 3],
    'b': {
        'c': 1,
        'd': {'e': 'f', 'f': (5, 6, 7)},
        'f': [7, [8, [9, 10]]],
        'i': 'hello',
    },
}
EXPECTED_RESULT = [1, 2, 3, 'hello', 1, 'f', 5, 6, 7, 7, 8, 9, 10]


def long_func(multiplier, int_value):
    time.sleep(1)
    return multiplier * int_value


def test1_func1(value, output=[]):
    if isinstance(value, (dict, list, tuple)):
        output_list = test1_func2(value, output)
        return output_list
    else:
        output.append(value)
        return output


def test1_func2(iterable_obj, output):
    if isinstance(iterable_obj, dict):
        for value in iterable_obj.values():
            output_list = test1_func1(value, output)
        return output_list
    else:
        for value in iterable_obj:
            output_list = test1_func1(value, output)
        return output_list


def test2_func1(func, ints):
    for value in ints:
        result = func(value)
        yield result


def test3_func1(dictionary):
    for value in test1_func1(dictionary, []):
        yield value


def test3_func2(iterable):
    for value in iterable:
        yield value


class TestTask5(unittest.TestCase):

    def compare_lists_ignore_order(self, test_list, expected_list):
        self.assertEqual(sorted(test_list, key=hash), sorted(expected_list, key=hash))

    def test_1(self):
        self.compare_lists_ignore_order(test1_func1(MY_DICT), EXPECTED_RESULT)

    def test_2(self):
        int_values = [random.randint(1, 100) for _ in range(5)]
        multiplier = random.randint(1, 100)
        test_func = functools.partial(long_func, multiplier)
        start_time = time.time()
        for i, result in enumerate(test2_func1(test_func, int_values)):
            if i == 0:
                first_result_elapsed_time = time.time() - start_time
                self.assertLess(first_result_elapsed_time, 2)
            self.assertEqual(int_values[i] * multiplier, result)
        else:
            self.assertEqual(i + 1, len(int_values))

    def test_3(self):
        result1 = test3_func1(MY_DICT)
        self.assertIsInstance(result1, types.GeneratorType)
        result2 = test3_func2(result1)
        self.assertIsInstance(result2, types.GeneratorType)
        self.compare_lists_ignore_order(list(result2), EXPECTED_RESULT)


if __name__ == '__main__':
    unittest.main(verbosity=2)
