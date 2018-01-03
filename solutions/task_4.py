#!/usr/bin/env python3
"""
TASK: Implement classes "Temperature", "Person" using Python descriptor protocols to execute unittests without errors.
"""
import re
import unittest
from collections import namedtuple
from datetime import datetime


class Temperature(object):

    def __init__(self, fahrenheit=0):
        self.fahrenheit = fahrenheit

    def _get_celsius(self):
        return (self.fahrenheit - 32)/1.8

    def _set_celsius(self, celsius):
        self.fahrenheit = celsius*1.8 + 32

    celsius = property(_get_celsius, _set_celsius)


FieldType = namedtuple('FieldType', ['name', 'type', 'formatter'])


class PersonFieldFormatter(object):

    @staticmethod
    def phone_format(phone):
        pattern = r"^[0-9]{3} [0-9]{2} [0-9]{7}$"
        if re.match(pattern, phone):
            return "+{} ({}) {}-{}-{}".format(phone[:3], phone[4:6], phone[7:10], phone[10:12], phone[12:])
        else:
            raise ValueError


class PersonFieldType(object):

    Birthday = FieldType('birthday', datetime, None)
    Name = FieldType('name', str, None)
    Phone = FieldType('phone', str, PersonFieldFormatter.phone_format)


class PersonField(object):

    def __init__(self, field_type):
        self.field = field_type

    def __get__(self, instance, owner):
        return instance.__dict__[self.field.name]

    def __set__(self, instance, attr_value):
        if not isinstance(attr_value, self.field.type):
            raise TypeError

        if self.field.formatter is not None:
            formatted_value = self.field.formatter(attr_value)
        else:
            formatted_value = attr_value

        instance.__dict__[self.field.name] = formatted_value


class Person(object):
    birthday = PersonField(PersonFieldType.Birthday)
    name = PersonField(PersonFieldType.Name)
    phone = PersonField(PersonFieldType.Phone)


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
