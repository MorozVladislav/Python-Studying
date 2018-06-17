from projects.automation_basics.http_client import HttpClient
import requests

URL = 'https://api.getchute.com/v2'


class TestClass(object):

    def test_1(self):
        client = HttpClient()
        response = client.get(URL)
        client.close()
        assert response.status_code == 200

    def test_2(self):
        client = HttpClient()
        client.get(URL, expected_rcode=200)

    def test_3(self):
        client = HttpClient()
        try:
            client.get(URL, timeout=0.001)
        except Exception as exc:
            assert isinstance(exc, requests.exceptions.ConnectTimeout)

    def test_4(self):
        client = HttpClient()
        response = client.get(URL, decode_json=True)
        assert type(response) == dict
