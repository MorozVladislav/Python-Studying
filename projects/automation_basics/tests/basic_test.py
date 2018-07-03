import os

from steps.github_api_steps import APISteps
from utils.http_client import HttpClient

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
        params = {'type': 'owner'}
        resp = client.get_user_repos(params=params, expected_code=200)
        assert int(resp.headers['X-RateLimit-Limit']) == 5000
        assert resp.json()[0]['has_projects'] is True

    def test_3(self):
        client = APISteps(host=HOST, user=USER, password=PASSWORD)
        client.get_token(['user', 'repo', 'delete_repo'])
        params = {'type': 'owner'}
        resp = client.get_user_repos(params=params, expected_code=200)
        assert int(resp.headers['X-RateLimit-Limit']) == 5000
        assert resp.json()[0]['has_projects'] is True
        client.delete_token()
