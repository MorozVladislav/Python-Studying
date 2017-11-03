#!/usr/bin/env python3
"""
TASK: Create 'Fake' class to run code below without errors.
"""

import random
import string


# INSERT YOUR CODE HERE


def generate_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


if __name__ == '__main__':
    fake = Fake()
    fake.non_existing_method('argument')
    fake.attribute
    fake[42]
    fake['non existing key']
    fake[generate_string()]
    fake2 = fake.blablabla('bla', bla='bla')
    fake2.whatever()
    fake2.whatever.again_whatever().and_again['foo']['bar'][1]
    getattr(fake2, generate_string())()()()()[generate_string()]()()()('lol')
