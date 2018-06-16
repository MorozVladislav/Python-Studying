import logging
import xml.etree.ElementTree as ET
from contextlib import contextmanager

import requests

logger = logging.getLogger(__name__)


class HttpClient(object):

    def __init__(self, host=None, base_url=None, headers=None, cookies=None, timeout=None, single_session=False):
        self.host = host
        self.base_url = base_url
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout
        self.single_session = single_session
        self._session = None

    @property
    def session(self):
        if self.single_session:
            if self._session is None:
                self._session = requests.session()
            return self._session
        else:
            return requests.session()

    @contextmanager
    def session_ctx(self):
        yield self.session
        if not self.single_session:
            self.session.close()

    def make_request(self, url, method='GET', return_json=False, return_tree=False, expected_response_code=None,
                     **kwargs):
        with self.session_ctx() as s:
            logger.debug('Making {} request, URL: {}, parameters: {}'.format(method, url, kwargs))
            resp = s.request(method, ''.join(filter(None, (self.host, self.base_url, url))), headers=self.headers,
                             cookies=self.cookies, timeout=self.timeout, **kwargs)
            logger.debug('Response received in {}.{} sec. Status code {}'.format(resp.elapsed.seconds,
                                                                                 resp.elapsed.microseconds,
                                                                                 resp.status_code))

            if expected_response_code is not None:
                if resp.status_code != expected_response_code:
                    logger.exception('Response code is {} but {} was expected'.format(resp.status_code,
                                                                                      expected_response_code))
                    raise Exception('Unexpected response code {}'.format(resp.status_code))

            if return_json:
                return resp.json()
            if return_tree:
                return ET.parse(resp.text)

            return resp

    def make_get_request(self, url, **kwargs):
        return self.make_request(url, method='GET', **kwargs)

    def make_post_request(self, url, **kwargs):
        return self.make_request(url, method='POST', **kwargs)

    def make_put_request(self, url, **kwargs):
        return self.make_request(url, method='PUT', **kwargs)

    def make_delete_request(self, url, **kwargs):
        return self.make_request(url, method='DELETE', **kwargs)

    def make_head_request(self, url, **kwargs):
        return self.make_request(url, method='HEAD', **kwargs)

    def make_options_request(self, url, **kwargs):
        return self.make_request(url, method='OPTIONS', **kwargs)

    def close(self):
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
