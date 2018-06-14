import requests
import logging

logger = logging.getLogger(__name__)


class HttpClient(object):

    def __init__(self, headers=None, cookies=None, timeout=None, base_api_url=None):
        self.headers = headers
        self.cookies = cookies
        self.timeout = timeout
        self.base_api_url = base_api_url

    def make_request(self, url, method='GET', return_json=False, expected_response_code=None, **kwargs):
        logger.debug('Making {} request, URL: {}, parameters: {}'.format(method, url, kwargs))
        with requests.session() as s:
            logger.debug('Opening session')
            resp = s.request(method, '{}{}'.format(self.base_api_url, url), headers=self.headers, cookies=self.cookies,
                             timeout=self.timeout, **kwargs)
            logger.debug('Response received')

            if expected_response_code is not None:
                if resp.status_code != expected_response_code:
                    logger.exception('Response code is {} but {} was expected'.format(resp.status_code,
                                                                                      expected_response_code))
                    raise Exception('Unexpected response code {}'.format(resp.status_code))

            logger.debug('Closing session')
            if return_json:
                logger.debug('Returning JSON response')
                return resp.json()

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
