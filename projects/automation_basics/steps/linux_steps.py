import logging

from utils.ssh_client import SSHClient

logger = logging.getLogger(__name__)


class LinuxSteps(SSHClient):

    def __init__(self,
                 host=None,
                 username=None,
                 password=None,
                 key=None,
                 passphrase=None,
                 use_key=False,
                 allow_unknown_hosts=False,
                 add_system_known_hosts=False,
                 environment=None,):

        super().__init__(host, username, password, key, passphrase, allow_unknown_hosts, environment)
        if add_system_known_hosts:
            self.add_system_known_hosts()
        self.connect(use_key=use_key)
        self.open_shell()

    def step(self, command, path, options=[], execute_in_shell=False, **kwargs):
        signature = [command]
        signature += options
        signature.append(path)
        str_signature = ' '.join(signature)
        if execute_in_shell:
            logger.info('Executing in shell {}'.format(str_signature))
            return self.execute_in_shell(str_signature, **kwargs)
        else:
            logger.info('Executing {}'.format(str_signature, **kwargs))
            return self.execute(str_signature)

    def cd(self, path, options=[], execute_in_shell=False, **kargs):
        return self.step('cd', path, options, execute_in_shell, **kargs)

    def mkdir(self, path, options=[], execute_in_shell=False, **kwargs):
        return self.step('mkdir', path, options, execute_in_shell, **kwargs)

    def rm(self, path, options=[], execute_in_shell=False, **kwargs):
        return self.step('rm', path, options, execute_in_shell, **kwargs)

    def ls(self, path, options=[], execute_in_shell=False, **kwargs):
        return self.step('ls', path, options, execute_in_shell, **kwargs)

    def cp(self, source, destination, options=[], execute_in_shell=False, **kwargs):
        return self.step('cp', ' '.join([source, destination]), options, execute_in_shell, **kwargs)

    def mv(self, source, directory, options=[], execute_in_shell=False, **kwargs):
        return self.step('mv', ' '.join([source, directory]), options, execute_in_shell, **kwargs)
