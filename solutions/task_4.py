#!/usr/bin/env python3
"""
TASK: Implement classes "Temperature", "Person" using Python descriptor protocols to execute unittests without errors.
"""
import re
import unittest
from datetime import datetime


class Temperature(object):

    def __init__(self, value=0):
        self.fahrenheit = value

    def get_celsius(self):
        return (self.fahrenheit - 32)/1.8

    def set_celsius(self, value):
        self.fahrenheit = value*1.8 + 32

    celsius = property(get_celsius, set_celsius)


class Descriptor(object):

    def __init__(self, attr_name, attr_type):
        self.attr_name = attr_name
        self.attr_type = attr_type

    def __get__(self, instance, owner):
        return instance.__dict__[self.attr_name]

    def __set__(self, instance, attr_value):
        if self.attr_type != type(attr_value):
            raise TypeError
        if self.attr_name == 'phone':
            pattern = r"[0-9]{3} [0-9]{2} [0-9]{7}$"
            if re.match(pattern, attr_value):
                instance.__dict__.__setitem__(self.attr_name, "+{} ({}) {}-{}-{}".format(attr_value[:3],
                                                                                         attr_value[4:6],
                                                                                         attr_value[7:10],
                                                                                         attr_value[10:12],
                                                                                         attr_value[12:]))
            else:
                raise ValueError
        else:
            instance.__dict__.__setitem__(self.attr_name, attr_value)


class Person(object):
    birthday = Descriptor('birthday', datetime)
    name = Descriptor('name', str)
    phone = Descriptor('phone', str)


class TestTask4(unittest.TestCase):

    def test_temperature(self):
        tmprt = Temperature(212)
        self.assertEqual(tmprt.fahrenheit, 212)
        self.assertEqual(tmprt.celsius, 100)
        tmprt.celsius = 0
        self.assertEqual(tmprt.fahrenheit, 32)
        self.assertEqual(tmprt.celsius, 0)

    def test_person(self):
        guido = Person()
        with self.assertRaises(TypeError):
            guido.birthday = 1956
        guido.birthday = datetime.strptime("1956-01-31", "%Y-%m-%d")
        self.assertEqual(guido.birthday, datetime.strptime("1956-01-31", "%Y-%m-%d"))
        with self.assertRaises(TypeError):
            guido.name = ('Guido', 'van', 'Rossum')
        guido.name = 'Guido van Rossum'
        self.assertEqual(guido.name, 'Guido van Rossum')
        with self.assertRaises(TypeError):
            guido.phone = 375291122000
        with self.assertRaises(ValueError):
            guido.phone = '375291122000'
        with self.assertRaises(ValueError):
            guido.phone = '375 29 11220F0'
        with self.assertRaises(ValueError):
            guido.phone = '375 29 11220000000'
        guido.phone = '375 29 1122000'
        self.assertEqual(guido.phone, '+375 (29) 112-20-00')


if __name__ == '__main__':
    unittest.main()
