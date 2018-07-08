import logging

from requests.auth import HTTPBasicAuth

from utils.http_client import HttpClient

logger = logging.getLogger(__name__)


def credentials_checkup(check_token=False):
    def wrapper(func):
        def wrapped(obj, *args, **kwargs):
            if check_token:
                if obj.use_token and obj.token is None:
                    logger.error('Token is empty')
                    raise AuthorizationError
            else:
                if obj.user is None or obj.password is None:
                    logger.error('Credentials are not specified')
                    raise AuthorizationError
            return func(obj, *args, **kwargs)
        return wrapped
    return wrapper


def user_login_checkup(func):
    def wrapped(obj, *args, **kwargs):
        if obj.user_login is None:
            obj.get_user_login()
        return func(obj, *args, **kwargs)
    return wrapped


class APISteps(HttpClient):

    def __init__(self, user=None, password=None, token=None, use_token=False, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.password = password
        self.token = token
        self.use_token = use_token
        self.authorization_id = None
        self.user_login = None

    @credentials_checkup(check_token=True)
    @credentials_checkup()
    def authorised_request(self, method, url, **kwargs):

        if self.use_token:
            auth = OAuthToken(self.token)
            return self.request(method, url, auth=auth, **kwargs)

        else:
            auth = HTTPBasicAuth(self.user, self.password)
            return self.request(method, url, auth=auth, **kwargs)

    @credentials_checkup()
    def get_token(self, scopes):

        auth = HTTPBasicAuth(self.user, self.password)
        payload = {
            'scopes': scopes,
            'note': '{} script'.format(__name__)
        }
        resp = self.post('authorizations', auth=auth, json=payload, expected_code=201)

        response = resp.json()
        self.authorization_id = response['id']
        self.token = response['token']

    @credentials_checkup()
    def delete_token(self, **kwargs):

        if self.token is None:
            logger.warning('Token is already empty')
            return

        self.use_token = False
        self.token = None
        auth = HTTPBasicAuth(self.user, self.password)
        return self.delete('/authorizations/{}'.format(self.authorization_id), auth=auth, expected_code=204, **kwargs)

    def get_user_login(self, **kwargs):
        self.user_login = self.authorised_request('GET', 'user', **kwargs).json()['login']
        return self.user_login

    def get_user_repos(self, **kwargs):
        return self.authorised_request('GET', 'user/repos', expected_code=200, **kwargs)

    def create_repo(self, name, description='', homepage='', private=False, has_issues=True, has_projects=True,
                    has_wiki=True, auto_init=False, gitignore_template='', license_template='', allow_squash_merge=True,
                    allow_merge_commit=True, allow_rebase_merge=True, **kwargs):
        payload = {
            'name': name,
            'description': description,
            'homepage': homepage,
            'private': private,
            'has_issues': has_issues,
            'has_projects': has_projects,
            'has_wiki': has_wiki,
            'auto_init': auto_init,
            'gitignore_template': gitignore_template,
            'license_template': license_template,
            'allow_squash_merge': allow_squash_merge,
            'allow_merge_commit': allow_merge_commit,
            'allow_rebase_merge': allow_rebase_merge
        }
        return self.authorised_request('POST', 'user/repos', json=payload, expected_code=201, **kwargs)

    @user_login_checkup
    def delete_repo(self, name, **kwargs):
        return self.authorised_request('DELETE', 'repos/{}/{}'.format(self.user_login, name), expected_code=204,
                                       **kwargs)

    @user_login_checkup
    def edit_repo(self, name, description='', homepage='', private=False, has_issues=True, has_projects=True,
                  has_wiki=True, default_branch=None, allow_squash_merge=True, allow_merge_commit=True,
                  allow_rebase_merge=True, archived=False, **kwargs):
        payload = {
            'name': name,
            'description': description,
            'homepage': homepage,
            'private': private,
            'has_issues': has_issues,
            'has_projects': has_projects,
            'has_wiki': has_wiki,
            'allow_squash_merge': allow_squash_merge,
            'allow_merge_commit': allow_merge_commit,
            'allow_rebase_merge': allow_rebase_merge,
            'archived': archived
        }
        if default_branch is not None:
            payload.update({'default_branch': default_branch})
        return self.authorised_request('PATCH', 'repos/{}/{}'.format(self.user_login, name), json=payload,
                                       expected_code=200, **kwargs)


class AuthorizationError(Exception):
    pass


class OAuthToken(object):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'token {}'.format(self.token)
        return r

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __ne__(self, other):
        return not self == other
