import re
import pdb

from utils.ssh_client import SSHClientException, ConnectionFailedException, ShellNotOpenedException


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

    def test_delete_known_hosts(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect()
        ssh_client.clear_host_keys()
        try:
            ssh_client.connect()
        except SSHClientException as exc:
            assert type(exc) == ConnectionFailedException
        try:
            ssh_client.connect()
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

    def test_execute_command(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect(use_key=True)
        stdin, stdout, stderr = ssh_client.execute("grep 'AGP' /boot/config-3.10.0-862.6.3.el7.x86_64")
        for line in stdout.readlines():
            if re.search(r'INTEL', line) is not None:
                assert re.split(r'=', line.strip('\n'))[1] == 'y'

    def test_execute_in_shell(self, ssh_client):
        ssh_client.add_system_known_hosts()
        ssh_client.connect(use_key=True)
        ssh_client.open_shell()
        result = ssh_client.execute_in_shell("grep 'AGP' /boot/config-3.10.0-862.6.3.el7.x86_64")
        lines = result.split('\r\n')
        for line in lines:
            if re.search(r'INTEL', line) is not None:
                assert re.split(r'=', line.strip('\n'))[1] == 'y'
        ssh_client.close_shell()
        try:
            ssh_client.execute_in_shell("grep 'AGP' /boot/config-3.10.0-862.6.3.el7.x86_64")
        except SSHClientException as exc:
            assert type(exc) == ShellNotOpenedException

    def test_cd_and_ls_steps(self, linux_client):
        linux_client.cd('/boot', execute_in_shell=True)
        result = linux_client.ls('./', options=['-al'], execute_in_shell=True)
        lines = result.split('\r\n')
        for line in lines:
            if re.search(r'config', line) is not None:
                assert ('config-3.10.0-862.6.3.el7.x86_64' or 'config-3.10.0-862.el7.x86_64') in line.split(' ')
