import logging
import xml.etree.ElementTree as XmlEtree
from contextlib import contextmanager

import requests

logger = logging.getLogger(__name__)


class HttpClient(object):

    GET, POST, PUT, DELETE, HEAD, OPTIONS = 'GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'

    def __init__(self, host='', base_url='', single_session=False, **kwargs):
        self.host = host
        self.base_url = base_url
        self.single_session = single_session
        self.kwargs = kwargs
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

    def request(self, method, url, decode_json=False, xml_tree=False, expected_rcode=None, **kwargs):
        self.kwargs.update(kwargs)
        with self.session_ctx() as s:
            logger.info('Making {} request, URL: {}, parameters: {}'.format(method, url, self.kwargs,))
            resp = s.request(method, str(self.host + self.base_url + url), **self.kwargs)
            logger.info('Request executed in {} sec. Response code {}'.format(resp.elapsed, resp.status_code))
            logger.debug(resp.text)

            if expected_rcode is not None:
                if resp.status_code != expected_rcode:
                    logger.error('Response code is {} but {} was expected'.format(resp.status_code, expected_rcode))
                    raise ValueError('Unexpected response code {}'.format(resp.status_code))

            if decode_json:
                return resp.json()
            if xml_tree:
                return XmlEtree.parse(resp.text)

            return resp

    def get(self, url, **kwargs):
        return self.request(self.GET, url, **kwargs)

    def post(self, url, **kwargs):
        return self.request(self.POST, url, **kwargs)

    def put(self, url, **kwargs):
        return self.request(self.PUT, url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(self.DELETE, url, **kwargs)

    def head(self, url, **kwargs):
        return self.request(self.HEAD, url, **kwargs)

    def options(self, url, **kwargs):
        return self.request(self.OPTIONS, url, **kwargs)

    def close(self):
        if self._session is not None:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
