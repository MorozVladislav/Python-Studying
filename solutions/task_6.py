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


def pair_sum_1(sequence, expected_sum):
    output = []
    for i in range(len(sequence)):
        for j in range(i + 1, len(sequence)):
            if sequence[i] + sequence[j] == expected_sum:
                output.append((sequence[i], sequence[j]))
    return output


def pair_sum_2(sequence, expected_sum):
    output = []
    while len(sequence) > 1:
        current_value = sequence[0]
        for i in range(1, len(sequence)):
            if current_value + sequence[i] == expected_sum:
                output.append((current_value, sequence[i]))
                sequence.remove(sequence[i])
                sequence.remove(current_value)
                break
            i += 1
        if sequence[0] == current_value:
            sequence.remove(sequence[0])
    return output


def largest_continuous_sum_1(sequence):
    max_sum = None
    i = len(sequence)
    while i > 0:
        for j in range(len(sequence) - i + 1):
            current_sum = sum(sequence[j:j + i])
            if max_sum is None or current_sum > max_sum:
                max_sum = current_sum
        i -= 1
    return max_sum


def convert_sequence_1(sequence, period=3):
    output = []
    i = 0
    j = 0
    while i + j < len(sequence):
        for j in range(0, len(sequence), period):
            output.append(sequence[i + j])
        i += 1
    return output


def convert_sequence_2(sequence, period=3):
    output = []
    while len(sequence) > 0:
        index_correction = 0
        for index in range(0, len(sequence), period):
            output.append(sequence[index - index_correction])
            sequence.remove(sequence[index - index_correction])
            index_correction += 1
        period -= 1
    return output


def get_inf_seq_element_1(index):
    counter, number_of_same_values, counter_of_same_values = 0, 0, 0
    value = True
    while counter <= index:
        if counter_of_same_values < number_of_same_values:
            output = value
            counter_of_same_values += 1
        else:
            output = value
            value = not value
            counter_of_same_values = 0
            number_of_same_values += 1
        counter += 1
    if output is True:
        return 1
    else:
        return 0


def get_inf_seq_element_2(index):
    counter_of_values, counter_of_same_values = 0, 0
    while counter_of_values <= index:
        counter_of_same_values += 1
        counter_of_values = counter_of_values + counter_of_same_values
    if counter_of_same_values % 2 == 0:
        return 0
    else:
        return 1


PAIR_SUM = [
    pair_sum_1,
    pair_sum_2,
]

LARGEST_CONTINUOUS_SUM = [
    largest_continuous_sum_1,
]

CONVERT_SEQUENCE = [
    convert_sequence_1,
    convert_sequence_2,
]

GET_INF_SEQ_ELEMENT = [
    get_inf_seq_element_1,
    get_inf_seq_element_2,
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
