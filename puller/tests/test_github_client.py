import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.github_client import GitHubClient


def test_github_client_initialization():
    client = GitHubClient("dummy_token")
    assert client._last_pull_time is None
    assert client._pull_status == {}


@pytest.mark.asyncio
async def test_pull_repository_success():
    client = GitHubClient("dummy_token")
    with patch('github.Github') as mock_github:
        mock_repo = Mock()
        mock_github.return_value.get_repo.return_value = mock_repo
        
        status = client.pull_repository("test/repo", "/tmp")
        
        assert status['success'] is True
        assert isinstance(status['timestamp'], datetime)
        assert "Successfully pulled test/repo" in status['message']


@pytest.mark.asyncio
async def test_pull_repository_failure():
    client = GitHubClient("dummy_token")
    with patch('github.Github') as mock_github:
        mock_github.return_value.get_repo.side_effect = Exception("Test error")
        
        status = client.pull_repository("test/repo", "/tmp")
        
        assert status['success'] is False
        assert isinstance(status['timestamp'], datetime)
        assert "Test error" in status['message']
