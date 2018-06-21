import json
import os

from projects.automation_basics.http_client import HttpClient

HOST = 'https://api.github.com/'
USER = os.environ['TEST_USER']
PASSWORD = os.environ['TEST_PASSWORD']
TOKEN = os.environ['TEST_TOKEN']


class TestClass(object):

    def test_1(self):
        client = HttpClient(host=HOST)
        resp = client.get('zen')
        assert resp.status_code == 200

    def test_2(self):
        client = HttpClient(host=HOST, user=USER, password=PASSWORD)
        resp = client.get('user')
        assert resp.status_code == 200
        assert int(resp.headers['X-RateLimit-Limit']) == 5000

    def test_3(self):
        client = HttpClient(host=HOST, user=USER, password=PASSWORD)
        params = {'type': 'owner'}
        resp = client.get('user/repos', params=params)
        d = json.loads(resp.text)
        assert resp.status_code == 200
        assert d[0]['has_projects'] is True

    def test_4(self):
        client = HttpClient(host=HOST, token=TOKEN)
        params = {'type': 'owner'}
        resp = client.get('user/repos', params=params)
        d = json.loads(resp.text)
        assert resp.status_code == 200
        assert d[0]['has_projects'] is True
