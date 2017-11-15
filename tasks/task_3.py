#!/usr/bin/env python3
"""
TASK: Implement decorators 'add_2', 'add_n', 'cached' and class 'Contact' to perform code below without errors.
"""
import time
from datetime import datetime, timedelta


# INSERT YOUR CODE HERE


CACHE_LIFE_TIME = 1


@add_2
def multiply_1(a, b):
    return a * b


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
    assert multiply_2(3, 4) == 17

    datetime1 = get_datetime_now()
    datetime2 = get_datetime_now()
    assert datetime1 == datetime2
    time.sleep(CACHE_LIFE_TIME)
    datetime3 = get_datetime_now()
    assert datetime1 < datetime3

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
