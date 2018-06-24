import json
import os
import random
import string

from projects.automation_basics.http_client import HttpClient

HOST = 'https://api.github.com/'
AUTH = os.environ['AUTH'].split(':')
TOKEN = None


class TestClass(object):

    def test_1(self):
        client = HttpClient(host=HOST)
        resp = client.get('zen')
        assert resp.status_code == 200

    def test_2(self):
        client = HttpClient(host=HOST, user=AUTH[0], password=AUTH[1])
        resp = client.get('user')
        assert resp.status_code == 200
        assert int(resp.headers['X-RateLimit-Limit']) == 5000

    def test_3(self):
        client = HttpClient(host=HOST, user=AUTH[0], password=AUTH[1])
        params = {'type': 'owner'}
        resp = client.get('user/repos', params=params)
        d = json.loads(resp.text)
        assert resp.status_code == 200
        assert d[0]['has_projects'] is True

    def test_4(self):
        client = HttpClient(host=HOST, user=AUTH[0], password=AUTH[1])
        fingerprint = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        params = {'type': 'owner'}
        payload = {'scopes': ['repo', 'user', 'delete_repo'], 'fingerprint': fingerprint, 'note': 'tests'}
        resp = client.post('authorizations', json=payload)
        assert resp.status_code == 201
        global TOKEN
        TOKEN = json.loads(resp.text)['token']
        client = HttpClient(host=HOST, token=TOKEN)
        resp = client.get('user/repos', params=params)
        d = json.loads(resp.text)
        assert resp.status_code == 200
        assert d[0]['has_projects'] is True
