import json
import logging
import pdb

from requests.auth import HTTPBasicAuth

from lib.http_client import HttpClient

logger = logging.getLogger(__name__)


class APISteps(HttpClient):

    def __init__(self, user=None, password=None, client_id=None, client_secret=None, token=None, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def authorised_request(self, method, url, **kwargs):
        if self.user is not None and self.password is not None:
            if self.client_id is not None or self.client_secret is not None or self.token is not None:
                logger.warning('Multiple authentication methods parameters are provided. Basic authentication '
                               'implemented by default')
            auth = HTTPBasicAuth(self.user, self.password)
            return super().request(method, url, auth=auth, **kwargs)
        elif self.client_id is not None and self.client_secret is not None:
            if self.token is not None:
                logger.warning('Multiple authentication methods parameters are provided. OAuth application '
                               'authentication implemented by default')
            params = {'client_secret': self.client_secret, 'note': '{} script'.format(__name__)}
            headers = {'Content-Length': '0'}
            resp = super().put('authorizations/clients/{}'.format(self.client_id), params=params, headers=headers)
            if resp.status_code == 200:
                logger.info('Existing token successfully received')
            if resp.status_code == 201:
                logger.info('A new token was created')
            pdb.set_trace()
            return super().request(method, url, token=json.dumps(resp.text)[0]['token'])
        elif self.token is not None:
            headers = {'Authorization': 'token {}'.format(self.token)}
            return super().request(method, url, headers=headers)
        else:
            logger.error('Authentication parameters are not specified')
            raise AuthenticationError

    def authorised_get_request(self, url, **kwargs):
        return self.authorised_request('GET', url, **kwargs)

    def authorised_post_request(self, url, **kwargs):
        return self.authorised_request('POST', url, **kwargs)

    def authorised_put_request(self, url, **kwargs):
        return self.authorised_request('PUT', url, **kwargs)

    def authorised_delete_request(self, url, **kwargs):
        return self.authorised_request('DELETE', url, **kwargs)

    def authorised_head_request(self, url, **kwargs):
        return self.authorised_request('HEAD', url, **kwargs)

    def authorised_options_request(self, url, **kwargs):
        return self.authorised_request('OPTIONS', url, **kwargs)


class AuthenticationError(Exception):
    pass
