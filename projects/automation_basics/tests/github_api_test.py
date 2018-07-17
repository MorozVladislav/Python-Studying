import pytest

from config import Config
from utils.http_client import HttpClient
from utils.http_client import UnexpectedStatusCode


class TestGitHubAPI(object):

    @pytest.fixture(autouse=True)
    def setup_api(self, github_api_steps):
        self.api = github_api_steps

    def teardown_method(self, _):
        try:
            self.api.delete_token()
        except UnexpectedStatusCode:
            pass
        try:
            self.api.delete_repo(Config.REPO_NAME)
        except UnexpectedStatusCode:
            pass

    def test_unauthorized_request(self):
        client = HttpClient(host=Config.HOST)
        resp = client.get('zen', expected_code=200)
        assert int(resp.headers['X-RateLimit-Limit']) == 60

    def test_authorized_request(self):
        params = {'type': 'owner'}
        resp = self.api.get_user_repos(params=params)
        assert int(resp.headers['X-RateLimit-Limit']) == 5000
        assert resp.json()[0]['has_projects'] is True

    def test_token_authorized_request(self):
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        params = {'type': 'owner'}
        resp = self.api.get_user_repos(params=params)
        assert int(resp.headers['X-RateLimit-Limit']) == 5000
        assert resp.json()[0]['has_projects'] is True

    def test_create_and_delete_repo(self):
        params = {'type': 'owner'}
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        resp = self.api.get_user_repos(params=params)
        repos_count = len(resp.json())
        repo_properties = {'description': Config.REPO_DESCRIPTION}
        resp = self.api.create_repo(Config.REPO_NAME, repo_properties)
        assert resp.json()['name'] == Config.REPO_NAME
        assert resp.json()['description'] == Config.REPO_DESCRIPTION
        resp = self.api.get_user_repos(params=params)
        assert len(resp.json()) == repos_count + 1
        self.api.delete_repo(Config.REPO_NAME)
        resp = self.api.get_user_repos(params=params)
        assert len(resp.json()) == repos_count

    def test_create_the_same_repo(self):
        params = {'type': 'owner'}
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        resp = self.api.get_user_repos(params=params)
        repos_count = len(resp.json())
        repo_properties = {'description': Config.REPO_DESCRIPTION}
        self.api.create_repo(Config.REPO_NAME, repo_properties)
        try:
            self.api.create_repo(Config.REPO_NAME, repo_properties)
        except UnexpectedStatusCode as exc:
            assert exc.status_code == 422
        resp = self.api.get_user_repos(params=params)
        assert len(resp.json()) == repos_count + 1

    def test_delete_nonexistent_repo(self):
        params = {'type': 'owner'}
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        resp = self.api.get_user_repos(params=params)
        repos_count = len(resp.json())
        try:
            self.api.delete_repo(Config.REPO_NAME)
        except UnexpectedStatusCode as exc:
            assert exc.status_code == 404
        resp = self.api.get_user_repos(params=params)
        assert len(resp.json()) == repos_count

    def test_edit_repo(self):
        edited_repo_description = 'Edited test repo'
        edited_repo_homepage = 'www.example.com'
        params = {'type': 'owner'}
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        resp = self.api.get_user_repos(params=params)
        repos_count = len(resp.json())
        repo_properties = {'description': Config.REPO_DESCRIPTION}
        self.api.create_repo(Config.REPO_NAME, repo_properties)
        repo_properties = {
            'description': edited_repo_description,
            'homepage': edited_repo_homepage,
            'has_issues': False,
            'has_projects': False,
            "has_wiki": False
        }
        self.api.edit_repo(Config.REPO_NAME, repo_properties)
        resp = self.api.get_user_repos(params=params)
        assert resp.json()[repos_count]['description'] == edited_repo_description
        assert resp.json()[repos_count]['homepage'] == edited_repo_homepage
        assert resp.json()[repos_count]['has_issues'] is False
        assert resp.json()[repos_count]['has_projects'] is False
        assert resp.json()[repos_count]['has_wiki'] is False

    def test_edit_nonexistent_repo(self):
        edited_repo_description = 'Edited test repo'
        edited_repo_homepage = 'www.example.com'
        self.api.get_token(['user', 'repo', 'delete_repo'])
        self.api.use_token = True
        repo_properties = {
            'description': edited_repo_description,
            'homepage': edited_repo_homepage,
            'has_issues': False,
            'has_projects': False,
            "has_wiki": False
        }
        try:
            self.api.edit_repo(Config.REPO_NAME, repo_properties)
        except UnexpectedStatusCode as exc:
            assert exc.status_code == 404
