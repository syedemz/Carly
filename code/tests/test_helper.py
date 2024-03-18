from code.carly_server.helper import execute_login, fetch_record, update_record
from code.carly_server.authorizer import generate_token
import pytest
from unittest.mock import patch, MagicMock

@patch('code.carly_server.helper.fetch_record')
def test_execute_login(mock_fetch_record):
    # Mock the fetch_record function
    mock_fetch_record.return_value = {'email': {'S': 'test@example.com'}, 'password': {'S': 'password123'}, 'customer_id': {'S': '123'}, 'language': {'S': 'en'}}


    # Call the function being tested
    result = execute_login('test@example.com', 'password123')

    # Assert the result
    assert result['customer_id'] ==  '123'
    assert result["language"] == 'en'


@patch('code.carly_server.helper.fetch_record')
def test_execute_login_with_missing_password(mock_fetch_record):
    # Mock the fetch_record function
    mock_fetch_record.return_value = {'email': {'S': 'test@example.com'}, 'customer_id': {'S': '123'}, 'language': {'S': 'en'}}
    # Call the function being tested
    result = execute_login('test@example.com', 'password123')

    # Assert the result
    assert result is None


@patch('code.carly_server.helper.fetch_record')
def test_update_record(mock_fetch_record):
     # Mock the fetch_record function
    mock_fetch_record.return_value = {'email': {'S': 'test@example.com'}, 'customer_id': {'S': '123'}, 'language': {'S': 'en'}}
    # Call the function being tested
    result = update_record('2345','test@example.com', {'password':'password123'})
    assert result is False
  


