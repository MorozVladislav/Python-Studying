#!/usr/bin/env python3
"""
TASK: Implement at least following classes to execute unittests without errors:

'MixInMeta':
    Metaclass which can be used to get ability to mix in classes.

'MixInBase':
    Class which can be inherited to get ability to mix in classes. (To compare with 'MixInMeta'.)

'DocStyleMeta':
    Metaclass which can be used to check doc-strings of methods in a class.

'CacheMeta':
    Metaclass which can be used to cache all methods in a class.
"""
import re
import time
import unittest
import types
from functools import wraps


class MixInBase(object):

    @classmethod
    def mix_in(cls, new_base):
        cls.__bases__ += (new_base,)


class MixInMeta(type):

    def mix_in(cls, new_base):
        cls.__bases__ += (new_base,)


class DocStyleMeta(type):

    def __new__(mcs, name, bases, dct):
        for key, value in dct.items():
            if isinstance(value, types.FunctionType) and re.search('__', key) is None:
                if value.__doc__ is None:
                    raise DocStyleError("'{}' has no documentation string.".format(key))
                if re.search('  ', value.__doc__) is not None:
                    raise DocStyleError("'{}' has more than one space delimiter between words in documentation "
                                        "string.".format(key))
                if re.search('[A-Z]', str(key)) is not None:
                    raise DocStyleError("'{}' has no snake-case style.".format(key))
        return super().__new__(mcs, name, bases, dct)


CACHE = {}  # Cache imitation.
CACHE_LIFE_TIME = 1  # Cache expiration time.


class Creature(object):  # Common parent class for "Man" and "Women", just to not duplicate "sound" method.

    def __init__(self, genus):
        self.genus = genus

    def sound(self, msg):
        return "{}: {}".format(self.genus, msg)


class Man(Creature, metaclass=MixInMeta):  # Metaclass is used to add "mix in" functionality.

    GENUS = 'Man'

    def __init__(self):
        super(Man, self).__init__(self.GENUS)


class Women(MixInBase, Creature):  # Inheritance is used to add "mix in" functionality.

    GENUS = 'Women'

    def __init__(self):
        super(Women, self).__init__(self.GENUS)


class SingMixin(object):  # Class that will be mixed in during tests.

    def sing(self, sound):
        return self.sound(sound)


class DocStyleError(Exception):  # Common error for all exceptions in "DocStyleMeta" class.
    pass


def cached(cache_life_time):  # Just your caching function from #task_3 to use in "CacheMeta".
    def wrapper(func):

        CACHE[func] = {}

        @wraps(func)
        def wrapped(*args, **kwargs):
            key = '|'.join([str(args), str(kwargs)])
            result, created_at = CACHE[func].get(key, (None, None))
            if created_at is None or (time.time() - created_at) >= cache_life_time:
                result = func(*args, **kwargs)
                CACHE[func][key] = [result, time.time()]
            return result
        return wrapped

    return wrapper


class CacheMeta(type):

    def __new__(mcs, name, bases, dct):
        for key, value in dct.items():
            if isinstance(value, types.FunctionType) and re.search('__', key) is None:
                dct[key] = cached(CACHE_LIFE_TIME)(value)
        return super().__new__(mcs, name, bases, dct)


class TimeProvider(object, metaclass=CacheMeta):  # Metaclass is used to cache all methods in the class.

    def get_time_now(self):
        return time.time()


class TestTask7(unittest.TestCase):

    def test_1(self):
        self.assertFalse(hasattr(Man, 'sing'))  # Check class attributes before mixing.
        Man.mix_in(SingMixin)
        self.assertTrue(hasattr(Man, 'sing'))  # Check class attributes after mixing.
        man = Man()
        self.assertTrue(hasattr(man, 'sing'))  # Check instance attributes after mixing.

        text = "Hey, I just met you, and this is crazy, but here's my number, so call me, maybe?"
        song = man.sing(text)
        self.assertEqual(song, "Man: {}".format(text))

    def test_2(self):
        self.assertFalse(hasattr(Women, 'sing'))  # Check class attributes before mixing.
        Women.mix_in(SingMixin)
        self.assertTrue(hasattr(Women, 'sing'))  # Check class attributes after mixing.
        women = Women()
        self.assertTrue(hasattr(women, 'sing'))  # Check instance attributes after mixing.

        text = "It's hard to look right at you, baaaabeh, but here's my number, so call me, maybe?"
        song = women.sing(text)
        self.assertEqual(song, "Women: {}".format(text))

    def test_3(self):
        # Try to declare class with error in doc-string:
        with self.assertRaises(DocStyleError) as err:

            class Creature(object, metaclass=DocStyleMeta):

                def __init__(self, genus):
                    self.genus = genus

                def sound(self, msg):
                    return "{}: {}".format(self.genus, msg)

        self.assertEqual(err.exception.args,
                         ("'sound' has no documentation string.",))

        # Try to declare class with error in doc-string:
        with self.assertRaises(DocStyleError) as err:

            class Creature(object, metaclass=DocStyleMeta):

                def __init__(self, genus):
                    self.genus = genus

                def sound(self, msg):
                    """sound          func"""
                    return "{}: {}".format(self.genus, msg)

        self.assertEqual(err.exception.args,
                         ("'sound' has more than one space delimiter between words in documentation string.",))

        # Try to declare class with error in doc-string:
        with self.assertRaises(DocStyleError) as err:

            class Creature(object, metaclass=DocStyleMeta):

                def __init__(self, genus):
                    self.genus = genus

                def SoundFunc(self, msg):
                    """sound func"""
                    return "{}: {}".format(self.genus, msg)

        self.assertEqual(err.exception.args,
                         ("'SoundFunc' has no snake-case style.",))

        # Successful class declaration:
        class Creature(object, metaclass=DocStyleMeta):

            def __init__(self, genus):
                self.genus = genus

            def sound_func(self, msg):
                """sound func"""
                return "{}: {}".format(self.genus, msg)

    def test_4(self):
        time_provider = TimeProvider()
        date1 = time_provider.get_time_now()
        date2 = time_provider.get_time_now()
        time.sleep(CACHE_LIFE_TIME)  # Wait for cache expiration.
        date3 = time_provider.get_time_now()
        self.assertEqual(date1, date2)
        self.assertLess(date1, date3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
