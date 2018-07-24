import logging
import time

import paramiko

logger = logging.getLogger(__name__)


class SSHClient(object):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 allow_unknown_hosts=False,
                 environment=None):

        self.host = host
        self.username = username
        self.password = password
        self.key = key
        self.passphrase = passphrase
        self.allow_unknown_hosts = allow_unknown_hosts
        self.environment = environment
        self.host_keys = paramiko.HostKeys()
        self.client = paramiko.SSHClient()
        self.host_keys = self.client.get_host_keys()
        self._shell = None

    def __del__(self):
        self.client.close()
        logger.info('SSH client was closed')

    @property
    def shell(self):
        if self._shell is None:
            message = 'Shell was not opened'
            logger.error(message)
            raise ShellNotOpenedException(message)
        return self._shell

    def add_system_known_hosts(self, path=None):
        self.client.load_system_host_keys(path)

    def clear_host_keys(self):
        self.host_keys.clear()

    def connect(self, use_key=False, *args, **kwargs):

        if self.allow_unknown_hosts:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.username is None:
            message = 'Username is not specified'.format(self.host)
            logger.error(message)
            raise ConnectionFailedException(message)

        try:
            if use_key:
                if self.key is None:
                    message = 'Private key file is not specified'.format(self.host)
                    logger.error(message)
                    raise ConnectionFailedException(message)
                self.client.connect(self.host, username=self.username, key_filename=self.key,
                                    passphrase=self.passphrase, *args, **kwargs)
            else:
                if self.password is None:
                    message = 'Password is not specified'.format(self.host)
                    logger.error(message)
                    raise ConnectionFailedException(message)
                self.client.connect(self.host, username=self.username, password=self.password, *args, **kwargs)

        except paramiko.SSHException:
            message = 'Failed to connect to {}'.format(self.host)
            logger.error(message)
            raise ConnectionFailedException(message)

    def execute(self, command, *args, **kwargs):
        return self.client.exec_command(command.strip('\n'), environment=self.environment, *args, **kwargs)

    def open_shell(self):
        self._shell = self.client.invoke_shell()
        logger.info('New shell was opened')

    def execute_in_shell(self, command):
        self.shell.send(command + '\n')
        result = self.shell.recv(1)
        while self.shell.recv_ready():
            result += self.shell.recv(1)
            if not self.shell.recv_ready():
                time.sleep(0.01)
        str_result = str(result, 'utf8')
        return str_result

    def close_shell(self):
        self.shell.close()
        self._shell = None
        logger.info('Current shell was closed')


class SSHClientException(Exception):
    pass


class ShellNotOpenedException(SSHClientException):
    pass


class ConnectionFailedException(SSHClientException):
    pass
