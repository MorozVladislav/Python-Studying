import os
import time
import pdb

from steps.github_api_steps import APISteps
from utils.http_client import HttpClient
from utils.http_client import UnexpectedStatusCode

HOST = 'https://api.github.com/'
USER = os.environ['GITHUB_USER']
PASSWORD = os.environ['GITHUB_PSWD']
CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']
REPO_NAME = 'test-repo'
REPO_DESCRIPTION = 'Just a test repo'


class TestClass(object):

    HTTP_CLIENT = None
    API_CLIENT = None
    RESP = None

    def teardown_method(self):
        if self.API_CLIENT is not None:
            try:
                self.API_CLIENT.delete_token()
            except UnexpectedStatusCode:
                pass
            try:
                self.API_CLIENT.delete_repo(REPO_NAME)
            except UnexpectedStatusCode:
                pass
            finally:
                self.API_CLIENT = None
                self.RESP = None

    def test_unauthorized_request(self):
        self.HTTP_CLIENT = HttpClient(host=HOST)
        self.RESP = self.HTTP_CLIENT.get('zen', expected_code=200)
        assert int(self.RESP.headers['X-RateLimit-Limit']) == 60

    def test_authorized_request(self):
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD)
        params = {'type': 'owner'}
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert int(self.RESP.headers['X-RateLimit-Limit']) == 5000
        assert self.RESP.json()[0]['has_projects'] is True

    def test_token_authorized_request(self):
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD, use_token=True)
        self.API_CLIENT.get_token(['user', 'repo', 'delete_repo'])
        params = {'type': 'owner'}
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert int(self.RESP.headers['X-RateLimit-Limit']) == 5000
        assert self.RESP.json()[0]['has_projects'] is True

    def test_create_and_delete_repo(self):
        params = {'type': 'owner'}
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD, use_token=True)
        self.API_CLIENT.get_token(['user', 'repo', 'delete_repo'])
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        repos_count = len(self.RESP.json())
        self.RESP = self.API_CLIENT.create_repo(REPO_NAME, description=REPO_DESCRIPTION)
        assert self.RESP.json()['name'] == REPO_NAME
        assert self.RESP.json()['description'] == REPO_DESCRIPTION
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert len(self.RESP.json()) == repos_count + 1
        self.API_CLIENT.delete_repo(REPO_NAME)

        # time.sleep(5)  # Why the server sometimes returns me a wrong amount of repos without this line?

        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert len(self.RESP.json()) == repos_count

    def test_create_the_same_repo(self):
        params = {'type': 'owner'}
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD, use_token=True)
        self.API_CLIENT.get_token(['user', 'repo', 'delete_repo'])
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        repos_count = len(self.RESP.json())
        self.API_CLIENT.create_repo(REPO_NAME, description=REPO_DESCRIPTION)
        try:
            self.API_CLIENT.create_repo(REPO_NAME, description=REPO_DESCRIPTION)
        except UnexpectedStatusCode as exc:
            assert exc.status_code == 422
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert len(self.RESP.json()) == repos_count + 1

    def test_delete_nonexistent_repo(self):
        params = {'type': 'owner'}
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD, use_token=True)
        self.API_CLIENT.get_token(['user', 'repo', 'delete_repo'])
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        repos_count = len(self.RESP.json())
        try:
            self.API_CLIENT.delete_repo(REPO_NAME)
        except UnexpectedStatusCode as exc:
            assert exc.status_code == 404
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert len(self.RESP.json()) == repos_count

    def test_edit_repo(self):
        edited_repo_description = 'Edited test repo'
        edited_repo_homepage = 'www.example.com'
        params = {'type': 'owner'}
        self.API_CLIENT = APISteps(host=HOST, user=USER, password=PASSWORD, use_token=True)
        self.API_CLIENT.get_token(['user', 'repo', 'delete_repo'])
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        repos_count = len(self.RESP.json())
        self.API_CLIENT.create_repo(REPO_NAME, description=REPO_DESCRIPTION)
        self.API_CLIENT.edit_repo(REPO_NAME, description=edited_repo_description, homepage=edited_repo_homepage,
                                  has_issues=False, has_projects=False, has_wiki=False)
        self.RESP = self.API_CLIENT.get_user_repos(params=params)
        assert self.RESP.json()[repos_count]['description'] == edited_repo_description
        assert self.RESP.json()[repos_count]['homepage'] == edited_repo_homepage
        assert self.RESP.json()[repos_count]['has_issues'] is False
        assert self.RESP.json()[repos_count]['has_projects'] is False
        assert self.RESP.json()[repos_count]['has_wiki'] is False
