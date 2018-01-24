#!/usr/bin/env python3
"""
TASK: Implement at least following functions to execute unittests without errors:

'pair_sum_1':
    Takes arguments: sequence, expected_sum.
    Returns all possible pairs (a, b) in the sequence where a + b = expected_sum.

'largest_continuous_sum_1':
    Takes arguments: sequence.
    Returns largest sum of continuous sequence among all possible sequences:
    sum(largest_seq) = max(sum(seq_1), sum(seq_2), sum(seq_3), ..., sum(seq_n))

'convert_sequence_1':
    Takes arguments: sequence, period.
    Converts sequence from [a1, a2, a3, b1, b2, b3, c1, c2, c3, ...]
                       to  [a1, b1, c1, ..., a2, b2, c2, ..., a3, b3, c3, ...]
    Period has default value = 3.

'get_inf_seq_element_1':
    Takes arguments: index.
    Return value with specified index in infinite sequence: [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, ...].

You can implement several solutions for each test and place functions in corresponding lists with functions.
"""
import unittest


# INSERT YOUR CODE HERE


PAIR_SUM = [
    pair_sum_1,
]

LARGEST_CONTINUOUS_SUM = [
    largest_continuous_sum_1,
]

CONVERT_SEQUENCE = [
    convert_sequence_1,
]

GET_INF_SEQ_ELEMENT = [
    get_inf_seq_element_1,
]


class TestTask6(unittest.TestCase):

    def test_1(self):
        sequence = [12, 56, 88, 3, 4, 44, 25, 13]
        target_sum = 16
        pairs_count = 2

        for func in PAIR_SUM:
            pairs = set(func(sequence, target_sum))
            self.assertEqual(len(pairs), pairs_count)
            for pair in pairs:
                self.assertEqual(sum(pair), target_sum)

    def test_2(self):
        sequence = [1, 5, -6, 6, 2, -3, -8, 9, 1, -1, 2, -9, 4]
        expected_sum = 11

        for func in LARGEST_CONTINUOUS_SUM:
            largest_sum = func(sequence)
            self.assertEqual(largest_sum, expected_sum)

    def test_3(self):
        sequence = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3', 'd1', 'd2', 'd3']
        expected_sequence = ['a1', 'b1', 'c1', 'd1', 'a2', 'b2', 'c2', 'd2', 'a3', 'b3', 'c3', 'd3']

        for func in CONVERT_SEQUENCE:
            result = func(sequence)
            self.assertListEqual(result, expected_sequence)

    def test_4(self):
        expected_sequence = [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        expected_values = [
            (10, 1),
            (100, 0),
            (1000, 1),
            (10000, 1),
            (100000, 1),
        ]

        for func in GET_INF_SEQ_ELEMENT:
            sequence = [func(i) for i in range(len(expected_sequence))]
            self.assertListEqual(sequence, expected_sequence)
            for idx, value in expected_values:
                self.assertEqual(func(idx), value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
