import os
import pdb

from lib.http_client import HttpClient
from steps.github_api_steps import APISteps

HOST = 'https://api.github.com/'
USER = os.environ['GITHUB_USER']
PASSWORD = os.environ['GITHUB_PSWD']
CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']


class TestClass(object):

    def test_1(self):
        client = HttpClient(host=HOST)
        resp = client.get('zen', expected_code=200)
        assert int(resp.headers['X-RateLimit-Limit']) == 60

    def test_2(self):
        client = APISteps(host=HOST, user=USER, password=PASSWORD)
        resp = client.authorised_get_request('user', expected_code=200)
        assert int(resp.headers['X-RateLimit-Limit']) == 5000

    def test_3(self):
        client = APISteps(host=HOST, user=USER, password=PASSWORD)
        params = {'type': 'owner'}
        resp = client.authorised_get_request('user/repos', params=params, json_to_iterable=True, expected_code=200)
        assert resp[0]['has_projects'] is True

    def test_4(self):
        client = APISteps(host=HOST, client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        params = {'type': 'owner'}
        resp = client.authorised_get_request('user/repos', params=params, json_to_iterable=True, expected_code=200)
        assert resp[0]['has_projects'] is True
