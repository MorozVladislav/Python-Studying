#!/usr/bin/env python3
"""
TASK: Implement decorators 'add_2', 'add_n', 'cached' and class 'Contact' to perform code below without errors.
"""
import time
from datetime import datetime, timedelta
from functools import wraps

CACHE = {}
CACHE_LIFE_TIME = 1


def add_2(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs) + 2
    return wrapped


def add_n(n):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs) + n
        return wrapped
    return wrapper


def cached(cache_life_time):
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


class Contact(object):
    def __init__(self, phone, operator):
        self._phone = phone
        self._operator = operator

    @property
    def phone(self):
        return ' '.join([self._phone[:-7], self._phone[-7:], self.operator])

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        self._operator = value


@cached(CACHE_LIFE_TIME)
@add_2
def multiply_1(a, b):
    return a * b


@cached(CACHE_LIFE_TIME)
@add_n(5)
def multiply_2(a, b):
    return a * b


@cached(CACHE_LIFE_TIME)
def get_datetime_now(add_timedelta=None):
    now = datetime.now()
    if add_timedelta:
        now += add_timedelta
    return now


if __name__ == '__main__':
    assert multiply_1(3, 4) == 14
    assert multiply_1.__name__ == 'multiply_1'
    assert multiply_2(3, 4) == 17
    assert multiply_2.__name__ == 'multiply_2'

    datetime1 = get_datetime_now()
    datetime2 = get_datetime_now()
    assert datetime1 == datetime2
    time.sleep(CACHE_LIFE_TIME)
    datetime3 = get_datetime_now()
    assert datetime1 < datetime3
    assert get_datetime_now.__name__ == 'get_datetime_now'

    datetime1 = get_datetime_now(add_timedelta=timedelta(hours=1))
    datetime2 = get_datetime_now(add_timedelta=timedelta(hours=1))
    assert datetime1 == datetime2

    datetime1 = get_datetime_now(add_timedelta=timedelta(days=1))
    datetime2 = get_datetime_now(add_timedelta=timedelta(days=2))
    assert datetime1 != datetime2

    c = Contact('80291112233', 'velcome')
    assert c.phone == '8029 1112233 velcome'
    c.phone = '80291113344'
    assert c.phone == '8029 1113344 velcome'
    c.operator = 'mts'
    assert c.phone == '8029 1113344 mts'
    assert c.operator == 'mts'
