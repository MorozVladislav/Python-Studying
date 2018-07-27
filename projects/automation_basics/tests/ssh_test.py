import re

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
        assert 'INTEL' in ssh_client.execute("grep 'AGP' /boot/config-3.10.0-862.6.3.el7.x86_64",
                                             raise_on_error=True).stdout

    def test_execute_in_shell(self, ssh_client):
        file = 'config-3.10.0-862.6.3.el7.x86_64'
        ssh_client.add_system_known_hosts()
        ssh_client.connect(use_key=True)
        ssh_client.open_shell()
        assert 'INTEL' in ssh_client.execute_in_shell("grep 'AGP' /boot/{}".format(file)).output
        ssh_client.close_shell()
        try:
            ssh_client.execute_in_shell("grep 'AGP' /boot/{}".format(file))
        except SSHClientException as exc:
            assert type(exc) == ShellNotOpenedException

    def test_cd_and_ls(self, linux_steps):
        file = 'config-3.10.0-862.6.3.el7.x86_64'
        result = linux_steps.ls('/boot/', options=['-al'], raise_on_error=True)
        assert file in result.stdout

        linux_steps.cd('/boot', execute_in_shell=True)
        assert file in linux_steps.ls('./', options=['-al'], execute_in_shell=True).output

    def test_mkdir_and_rm(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        assert 'test_dir' in linux_steps.ls('~/', raise_on_error=True).stdout
        linux_steps.rm('~/test_dir', options=['-r'], raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout

        linux_steps.mkdir('test_dir', execute_in_shell=True)
        assert 'test_dir' in linux_steps.ls('./', execute_in_shell=True)
        linux_steps.rm('test_dir', options=['-r'], execute_in_shell=True)
        assert 'test_dir' not in linux_steps.ls('./', execute_in_shell=True)

    def test_cp(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        linux_steps.cp('~/test_dir', '/', options=['-r'], raise_on_error=True)
        assert 'test_dir' in linux_steps.ls('/', raise_on_error=True).stdout
        linux_steps.rm('~/test_dir', options=['-rf'], raise_on_error=True)
        linux_steps.rm('/test_dir', options=['-rf'], raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout
        assert 'test_dir' not in linux_steps.ls('/', raise_on_error=True).stdout

        linux_steps.mkdir('test_dir', execute_in_shell=True)
        linux_steps.cp('./test_dir', '/', options=['-r'], execute_in_shell=True)
        assert re.search(r'test_dir', linux_steps.ls('/', execute_in_shell=True)) is not None
        linux_steps.rm('/test_dir', options=['-rf'], execute_in_shell=True)
        linux_steps.rm('./test_dir', options=['-rf'], execute_in_shell=True)
        assert re.search(r'test_dir', linux_steps.ls('/', execute_in_shell=True)) is None
        assert re.search(r'test_dir', linux_steps.ls('./', execute_in_shell=True)) is None

    def test_mv(self, linux_steps):
        linux_steps.mkdir('~/test_dir', raise_on_error=True)
        linux_steps.mv('~/test_dir', '~/new_dir', raise_on_error=True)
        assert 'test_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout
        assert 'new_dir' in linux_steps.ls('~/', raise_on_error=True).stdout
        linux_steps.rm('~/new_dir', options=['-rf'], raise_on_error=True)
        assert 'new_dir' not in linux_steps.ls('~/', raise_on_error=True).stdout

        linux_steps.mkdir('test_dir', execute_in_shell=True)
        linux_steps.mv('test_dir', 'new_dir', execute_in_shell=True)
        assert re.search(r'test_dir', linux_steps.ls('./', execute_in_shell=True)) is None
        assert re.search(r'new_dir', linux_steps.ls('./', execute_in_shell=True)) is not None
        linux_steps.rm('./new_dir', options=['-rf'], execute_in_shell=True)
        assert re.search(r'new_dir', linux_steps.ls('./', execute_in_shell=True)) is None
