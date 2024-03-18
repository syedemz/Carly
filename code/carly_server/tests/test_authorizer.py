import sys
sys.path.append("..")
from authorizer import check_client_version, generate_token
import pytest
import jwt
import datetime
import json



SECRET_KEY = 'carly-backend'

@pytest.mark.parametrize("version", [
    "2.1.0",
    "2.1.1",
    "3.0.0",
    "10.5.3"
])
def test_valid_version(version):
    assert check_client_version(version) is True

# Test cases for invalid version numbers
@pytest.mark.parametrize("version", [
    "2.0.9",  # Lower than required
    "2.0.0",  # Lower than required
    "1.9.9",  # Lower than required
    "2.1",    # Incomplete version number
    "2.1.",   # Incomplete version number
    "2",      # Incomplete version number
    "2.a.0",  # Invalid format
    "2.1.a",  # Invalid format
    "2..0",   # Invalid format
    "2.1.-1"  # Invalid format
])
def test_invalid_version(version):
    assert check_client_version(version) is False

# Test case for non-string input
def test_non_string_input():
    assert check_client_version(2.1) is False

# Test case for empty string input
def test_empty_string_input():
    assert check_client_version("") is False

# Test case for invalid 
def test_special_string_input():
    assert check_client_version("2.1.@") is False


####### Test Token Generation ###################
def test_generate_token():
    email = 'test@example.com'
    token = generate_token(email)
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    assert payload['email'] == email


    


