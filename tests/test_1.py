#!/usr/bin/env python3
"""
There is a kingdom with a king. Kingdom has its own territory with a border. The height of a terrain at the border is
denoted with a list of integers A. A value from the list A[p] means: when its negative - the terrain level is below the
sea level, when its positive - the terrain level is above the sea level, when its 0 - the terrain is at the sea level
height. The king wants to build a castle at each valley and hill along the border of his kingdom. Some part of terrain
is considered to be a valley when A[p - 1] > A[p]...A[q] < A[q + 1] where q >= p. On the other hand another part of
terrain is considered to be a hill when A[p - 1] < A[p]...A[q] > A[q + 1]  where q >= p. For beginning and ending of the
A condition for potential valley or hill is considered to be true. The task is to create a function intended to help the
king to calculate the number of castles needed. For the list of the same values the function shall return 1 as it is
considered to be a hill and valley simultaneously.
"""

import unittest

BORDER_HEIGHT = {
    'kingdom_1': [1, 2, 2, 3, 2, 3, 2, 2, 1, 1, 1, 2, 3, 3, 4, 4, 5, 4, 4, 3, 3, 4, 3, 2],
    'kingdom_2': [-3, -3, -4, -5, -4, -3, -2, -2, -2, -1, 0, 1, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 2, 3, 2, 2],
    'kingdom_3': [-5, -5],
    'kingdom_4': [1],
}
EXPECTED_OUTPUT = {
    'kingdom_1': 9,
    'kingdom_2': 8,
    'kingdom_3': 1,
    'kingdom_4': 1,
}


def castles_number(heights):
    start_height, current_height = None, None
    castles = 0

    if len(heights) == 0:
        raise Exception
    if len(heights) == 1:
        return 1

    for i in range(len(heights)):
        if current_height is None:
            current_height = heights[i]

        if heights[i] != current_height:
            if start_height is None:
                castles += 1
                start_height = heights[i]
                current_height = None
                continue
            if (heights[i] < current_height and start_height < current_height) or \
                    (heights[i] > current_height and start_height > current_height):
                castles += 1
                start_height = heights[i - 1]
                current_height = heights[i]
                continue
            if (heights[i] < current_height and start_height >= current_height) or \
                    (heights[i] > current_height and start_height <= current_height):
                start_height = heights[i - 1]
                current_height = heights[i]

        if heights[i] == current_height and i == len(heights) - 1:
            castles += 1

    return castles


def get_castles_number(border):
    if len(border) == 0:
        raise Exception
    if len(set(border)) == 1:
        return 1

    castles = 2
    curr_direction, prev_direction = None, None

    for i in range(1, len(border)):
        if border[i] > border[i - 1]:
            curr_direction = 1
        elif border[i] < border[i - 1]:
            curr_direction = -1

        if prev_direction is None:
            prev_direction = curr_direction
            continue

        if curr_direction + prev_direction == 0:
            castles += 1
            prev_direction = curr_direction

    return castles


class TestTask(unittest.TestCase):

    def test_1(self):
        for key, value in BORDER_HEIGHT.items():
            self.assertEqual(EXPECTED_OUTPUT[key], castles_number(value))
            self.assertEqual(EXPECTED_OUTPUT[key], get_castles_number(value))


if __name__ == '__main__':
    unittest.main(verbosity=2)
