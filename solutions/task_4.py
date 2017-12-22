#!/usr/bin/env python3
"""
TASK: Implement classes "Temperature", "Person" using Python descriptor protocols to execute unittests without errors.
"""
import re
import unittest
from datetime import datetime


class Temperature(object):

    def __init__(self, fahrenheit=0):
        self.fahrenheit = fahrenheit

    def _get_celsius(self):
        return (self.fahrenheit - 32)/1.8

    def _set_celsius(self, celsius):
        self.fahrenheit = celsius*1.8 + 32

    celsius = property(_get_celsius, _set_celsius)


class PersonField(object):

    def __init__(self, attrname, attrtype):
        self.attrname = attrname
        self.attrtype = attrtype

    def __get__(self, instance, owner):
        return instance.__dict__[self.attrname]

    def __set__(self, instance, attrvalue):
        if type(attrvalue) is not self.attrtype:
            raise TypeError
        if self.attrname == 'phone':
            pattern = r"^[0-9]{3} [0-9]{2} [0-9]{7}$"
            if re.match(pattern, attrvalue):
                instance.__dict__[self.attrname] = "+{} ({}) {}-{}-{}".format(attrvalue[:3],
                                                                              attrvalue[4:6],
                                                                              attrvalue[7:10],
                                                                              attrvalue[10:12],
                                                                              attrvalue[12:])
            else:
                raise ValueError
        else:
            instance.__dict__[self.attrname] = attrvalue


class PersonFieldType(object):
    Birthday = ('birthday', datetime)
    Name = ('name', str)
    Phone = ('phone', str)


class Person(object):
    birthday = PersonField(*PersonFieldType.Birthday)
    name = PersonField(*PersonFieldType.Name)
    phone = PersonField(*PersonFieldType.Phone)


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
