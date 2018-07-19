import pytest

import api_tests_config
import ssh_tests_config
from steps.github_api_steps import GitHubAPISteps
from utils.ssh_client import SSHClient


@pytest.fixture
def github_api_steps():
    return GitHubAPISteps(host=api_tests_config.APITestsConfig.HOST,
                          login=api_tests_config.APITestsConfig.LOGIN,
                          password=api_tests_config.APITestsConfig.PASSWORD)


@pytest.fixture
def ssh_client():
    return SSHClient(host=ssh_tests_config.SSHTestsConfig.HOST,
                     username=ssh_tests_config.SSHTestsConfig.USERNAME,
                     password=ssh_tests_config.SSHTestsConfig.PASSWORD,
                     key=ssh_tests_config.SSHTestsConfig.KEY,
                     passphrase=ssh_tests_config.SSHTestsConfig.PASSPHRASE)
