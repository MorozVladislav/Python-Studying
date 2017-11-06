#!/usr/bin/env python3
"""
TASK: Create 'Fake' class to run code below without errors.
"""

import random
import string


class Fake(dict):
    def __getattr__(self, name):
        print("Non existing attribute {} has been called".format(name))
        return self

    def __call__(self, *args, **kwargs):
        try:
            dict.__call__(*args, **kwargs)
            return self
        except (TypeError, ValueError):
            print("The attribute has been called with:")
            if len(args) > 0:
                print("- positional arguments: {}".format(str(", ".join(args))))
            else:
                print("- no positional arguments")
            if len(kwargs) > 0:
                kwargs_list = []
                for k, v in kwargs.items():
                    kwargs_list.append(str(k) + " = " + str(v))
                print("- keyword arguments: {}".format(str(", ".join(kwargs_list))))
            else:
                print("- no keyword arguments")
            return self

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            print("Unexisting key {} has been called".format(item))
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
