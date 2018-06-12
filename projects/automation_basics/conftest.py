import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope='module')
def https_connection_1():
    from http.client import HTTPSConnection
    connection = HTTPSConnection('www.python.org')
    connection.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='module')
def https_connection_2():
    from http.client import HTTPSConnection
    connection = HTTPSConnection('www.python.org')
    connection.connect()
    return connection
