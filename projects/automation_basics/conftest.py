import pytest

from config import Config
from steps.github_api_steps import GitHubAPISteps


@pytest.fixture
def github_api_steps():
    return GitHubAPISteps(host=Config.HOST, login=Config.LOGIN, password=Config.PASSWORD)
