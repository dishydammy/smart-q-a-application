import pytest
from unittest.mock import MagicMock
from smart_qa.client import LLMClient

@pytest.fixture
def mock_client(mocker):
    # Mock the LLMClient to avoid real API calls during tests
    mocker.patch('google.generativeai.configure')
    mocker.patch('google.generativeai.GenerativeModel')

    client = LLMClient()

    client._call_api = MagicMock(return_value='Mocked Response')
    return client