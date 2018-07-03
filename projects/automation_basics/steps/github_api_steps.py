import logging
import random
import string

from requests.auth import HTTPBasicAuth

from utils.http_client import HttpClient

logger = logging.getLogger(__name__)


class APISteps(HttpClient):

    def __init__(self, user=None, password=None, token=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.password = password
        self.token = token
        self.authorization_id = None

    def authorised_request(self, method, url, **kwargs):

        if self.token is not None:
            auth = OAuthToken(self.token)
            return self.request(method, url, auth=auth, **kwargs)

        elif self.user is not None and self.password is not None:
            auth = HTTPBasicAuth(self.user, self.password)
            return self.request(method, url, auth=auth, **kwargs)

        else:
            logger.error('Authentication parameters are not specified')
            raise AuthenticationError

    def get_token(self, scopes):

        if self.user is None or self.password is None:
            logger.error('Authentication parameters are not specified')
            raise AuthenticationError

        auth = HTTPBasicAuth(self.user, self.password)
        fingerprint = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        payload = {'scopes': scopes, 'fingerprint': fingerprint, 'note': '{} script'.format(__name__)}
        resp = self.post('authorizations', auth=auth, json=payload)

        if resp.status_code == 201:
            logger.info('New authorization token was received')
        else:
            logger.error('Failed to receive authorization token')
            raise AuthenticationError

        self.authorization_id = resp.json()['id']
        self.token = resp.json()['token']

    def delete_token(self):

        if self.user is None or self.password is None:
            logger.error('Authentication parameters are not specified')
            raise AuthenticationError

        if self.token is None:
            logger.warning('Token is already empty')
            return

        auth = HTTPBasicAuth(self.user, self.password)
        resp = self.delete('/authorizations/{}'.format(self.authorization_id), auth=auth)
        if resp.status_code == 204:
            logger.info('Token was successfully deleted')
        else:
            logger.error('Failed to delete token')
            raise AuthenticationError

    def get_user_repos(self, **kwargs):
        return self.authorised_request('GET', 'user/repos', **kwargs)


class AuthenticationError(Exception):
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
