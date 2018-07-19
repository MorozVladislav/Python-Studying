import pdb

from utils.ssh_client import SSHClientException, ConnectionFailedException


class TestSSH(object):

    def test_connection_to_unknown_host(self, ssh_client):
        try:
            ssh_client.connect()
        except SSHClientException as exc:
            assert type(exc) == ConnectionFailedException
        try:
            ssh_client.connect(use_key=True)
        except SSHClientException as exc:
            assert type(exc) == ConnectionFailedException

    def test_connection_allowing_unknown_hosts(self, ssh_client):
        ssh_client.allow_unknown_hosts = True
        ssh_client.connect()
        ssh_client.connect(use_key=True)

    def test_connection_to_system_known_host(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect()
        ssh_client.connect(use_key=True)
