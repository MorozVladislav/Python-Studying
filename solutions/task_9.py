#!/usr/bin/env python3
"""
TASK: Implement following context managers to execute unittests without errors:
class 'MyHttpCtxManagerClass'
function 'my_http_ctx_manager_func'
"""
import unittest
from contextlib import contextmanager
from http.client import HTTPSConnection, HTTPConnection, NotConnected

HTTPConnection.auto_open = False


class MyHttpCtxManagerClass:

    def __init__(self, url):
        self.url = url

    def __enter__(self):
        self.connection = HTTPSConnection(self.url)
        self.connection.connect()
        return self.connection

    def __exit__(self, *args):
        self.connection.close()


@contextmanager
def my_http_ctx_manager_func(url):
    connection = HTTPSConnection(url)
    connection.connect()
    yield connection
    connection.close()


CTX_MANAGERS = [
    MyHttpCtxManagerClass,
    my_http_ctx_manager_func,
]


class TestTask9(unittest.TestCase):

    def test_1(self):
        for ctx_manager in CTX_MANAGERS:

            with ctx_manager('www.python.org') as conn:
                self.assertIsInstance(conn, (HTTPSConnection, HTTPConnection))

                conn.request('GET', '/')
                resp1 = conn.getresponse()
                data1 = resp1.read()
                self.assertEqual(resp1.status, 200)
                self.assertIn(b'<title>Welcome to Python.org</title>', data1)

                conn.request('GET', '/jobs/')
                resp2 = conn.getresponse()
                data2 = resp2.read()
                self.assertEqual(resp2.status, 200)
                self.assertIn(b'<title>Python Job Board | Python.org</title>', data2)

            with self.assertRaises(NotConnected):
                conn.request('GET', '/community/')


if __name__ == '__main__':
    unittest.main(verbosity=2)
