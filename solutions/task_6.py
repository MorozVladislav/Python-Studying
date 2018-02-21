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
from itertools import cycle
from math import sqrt, floor


def pair_sum_1(sequence, expected_sum):
    output = []
    for first_summand_index in range(len(sequence)):
        for second_summand_index in range(first_summand_index + 1, len(sequence)):
            if sequence[first_summand_index] + sequence[second_summand_index] == expected_sum:
                output.append((sequence[first_summand_index], sequence[second_summand_index]))
    return output


def pair_sum_2(arr, k):
    pairs = []
    sorted_arr = sorted(arr)
    left, right = (0, len(sorted_arr)-1)
    while left < right:
        current_sum = sorted_arr[left] + sorted_arr[right]
        if current_sum == k:
            pairs.append((sorted_arr[left], sorted_arr[right]))
            left += 1  # Or right -= 1
        elif current_sum < k:
            left += 1
        else:
            right -= 1
    return pairs


def pair_sum_3(arr, k):
    pairs = []
    seen = set()
    for num in arr:
        target = k - num
        if target not in seen:
            seen.add(num)
        else:
            pairs.append((num, target))
    return pairs


def largest_continuous_sum_1(sequence):
    max_sum = None
    for subsequence_length in range(len(sequence), 0, -1):
        for subsequence_start_index in range(len(sequence) - subsequence_length + 1):
            current_sum = sum(sequence[subsequence_start_index:subsequence_start_index + subsequence_length])
            if max_sum is None or current_sum > max_sum:
                max_sum = current_sum
    return max_sum


def largest_continuous_sum_2(arr):
    max_sum = current_sum = arr[0]
    for num in arr[1:]:
        current_sum = max(current_sum + num, num)
        max_sum = max(current_sum, max_sum)
    return max_sum


def convert_sequence_1(sequence, period=3):
    output = []
    for start_index in range(period):
        for index in range(start_index, len(sequence), period):
            output.append(sequence[index])
    return output


def convert_sequence_2(sequence, period=3):
    output = []
    sublists = [[] for _ in range(period)]
    index = cycle(range(period))
    for element in sequence:
        sublists[next(index)].append(element)
    for sublist in sublists:
        output += sublist
    return output


def convert_sequence_3(arr, period=3):
    n = len(arr) // period
    return [arr[(i % n * 3) + (i // n)] for i in range(len(arr))]


def convert_sequence_4(arr, period=3):
    res = []
    n = len(arr) // period
    for i in range(period):
        for j in range(n):
            res.append(arr[j * period + i])
    return res


def get_inf_seq_element_1(index):
    counter, number_of_same_values, counter_of_same_values = 0, 0, 0
    value = 1
    while counter < index:
        if counter_of_same_values < number_of_same_values:
            counter_of_same_values += 1
        else:
            value = value ^ 1
            counter_of_same_values = 0
            number_of_same_values += 1
        counter += 1
    return value


def get_inf_seq_element_2(index):
    counter_of_values, counter_of_same_values = 0, 0
    while counter_of_values <= index:
        counter_of_same_values += 1
        counter_of_values += counter_of_same_values
    return 0 if counter_of_same_values % 2 == 0 else 1


get_inf_seq_element_3 = lambda index: 1 if floor((sqrt(1.0 + 8.0*index) + 1.0)/2.0) % 2 else 0


def get_inf_seq_element_4(idx):
    curr_idx = 0
    result = 1
    next_period_len = 2
    while True:
        if idx <= curr_idx:
            return result
        else:
            result = 0 if result == 1 else 1
            curr_idx += next_period_len
            next_period_len += 1


PAIR_SUM = [
    pair_sum_1,
    pair_sum_2,
    pair_sum_3,
]

LARGEST_CONTINUOUS_SUM = [
    largest_continuous_sum_1,
    largest_continuous_sum_2,
]

CONVERT_SEQUENCE = [
    convert_sequence_1,
    convert_sequence_2,
    convert_sequence_3,
    convert_sequence_4,
]

GET_INF_SEQ_ELEMENT = [
    get_inf_seq_element_1,
    get_inf_seq_element_2,
    get_inf_seq_element_3,
    get_inf_seq_element_4,
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
