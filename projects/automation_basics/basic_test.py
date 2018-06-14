import logging


logger = logging.getLogger(__name__)


def func_1(connection):
    connection.request('GET', '/')
    resp = connection.getresponse()
    logger.info(resp.status)
    return resp


def func_2(connection):
    connection.request('GET', '/')
    resp = connection.getresponse()
    logger.info(resp.status)
    connection.close()
    return resp


class TestClass(object):
    def test_func_1(self, https_connection_1):
        assert func_1(https_connection_1).status == 200

    def test_func_2(self, https_connection_2):
        assert func_1(https_connection_2).status == 200

    def test_answer(self, cmdopt):
        if cmdopt == "type1":
            print("first")
        elif cmdopt == "type2":
            print("second")
        # assert 0  # to see what was printed
