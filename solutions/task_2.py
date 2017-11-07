#!/usr/bin/env python3
"""
TASK: Create 'Fake' class to run code below without errors.
"""

import random
import string


class Fake(object):
    def __getattr__(self, name):
        print("Non existing attribute {} has been called".format(name))
        return self

    def __call__(self, *args, **kwargs):
        try:
            super().__call__(self, *args, **kwargs)
            return self
        except AttributeError:
            print("The attribute has been called with:")
            if args:
                print("- positional arguments: {}".format(args))
            else:
                print("- no positional arguments")
            if kwargs:
                print("- keyword arguments: {}".format(kwargs))
            else:
                print("- no keyword arguments")
            return self

    def __getitem__(self, item):
        print("Attempt to get nonexistent key {}".format(item))
        return self


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
