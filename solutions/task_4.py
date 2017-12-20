#!/usr/bin/env python3
"""
TASK: Implement classes "Temperature", "Person" using Python descriptor protocols to execute unittests without errors.
"""
import unittest
from datetime import datetime


# INSERT YOUR CODE HERE


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
