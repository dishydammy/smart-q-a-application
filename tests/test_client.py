import pytest
from smart_qa.custom_exceptions import LLMAPIError

def test_summarize_caching(mock_client):
    text = "This is a test text for summarization."

    # First call
    mock_client.summarize(text)

    #Second call - should hit the cache
    mock_client.summarize(text)

    mock_client._call_api.assert_called_once()

def test_ask_different_questions(mock_client):
    context = "My name is Damola."

    # Call 1
    mock_client.ask(context, "Who are you")
    # Call 2
    mock_client.ask(context, "What is your name?")

    assert mock_client._call_api.call_count == 2

def test_extract_entities_json_cleaning(mock_client):
    mock_client._call_api.return_value = "```json\n{\"name\": \"Damola\"}\n```"

    result = mock_client.extract_entities("Some text")

    assert isinstance(result, dict)
    assert result["name"] == "Damola"