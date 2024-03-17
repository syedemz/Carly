from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import request, jsonify
from info_logger import global_logger

# Secret key used to sign the JWT token
SECRET_KEY = 'carly-backend'

def check_client_version(version: str) -> bool:
    """_summary_

    Args:
        version (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    required_version = [2, 1, 0]  # Minimum required version
    try:
        # Split the version string into its components
        provided_version = version.split('.')
        # Convert version components to integers
        provided_version = [int(part) for part in provided_version]
        if(len(provided_version) != len(required_version)):
            return False
        if(provided_version == required_version):
            return True
        # Compare each component
        for provided, required in zip(provided_version, required_version):
            if provided < required:
                return False
            elif provided > required:
                return True
    except ValueError as e:
        global_logger('Client Error', 'error', f"Invalid version number provided: {str(e)}")
        return False
    except AttributeError as e:
        global_logger('Client Error', 'error', f"version number must be a string: {str(e)}")
        return False

# Function to generate a JWT token
def generate_token(email: str) -> str:
    """_summary_

    Args:
        email (str): _description_

    Returns:
        object: _description_
    """
    expiration_time = datetime.utcnow() + timedelta(hours=3)
    payload = {
        'email': email,
        'exp': expiration_time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


# Decorator function to validate JWT token
def token_required(func):
    """_summary_

    Args:
        func (_type_): _description_

    Returns:
        _type_: _description_
    """
    @wraps(func)
    def validate_token(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            global_logger('Client Error', 'error', "Token is missing")
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Decode and verify the token
            payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as e:
            global_logger('Client Error', 'error', f"Token has expired: {str(e)}")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            global_logger('Client Error', 'error', f"Invalid Token: {str(e)}")
            return jsonify({'error': 'Invalid token'}), 401

        return func(*args, **kwargs)

    return validate_token


def require_version(func):
    """_summary_

    Args:
        func (_type_): _description_

    Returns:
        _type_: _description_
    """
    @wraps(func)
    def validate_version(*args, **kwargs):
        version = request.headers.get('version')

        if version:
            if not check_client_version(version):
                global_logger('Client Error', 'error', "Incorrect client version, please make sure you are using minimum 2.1.0")
                return jsonify({"error": "Incorrect client version, please make sure you are using minimum 2.1.0"}), 400
        else:
            global_logger('Client Error', 'error', "Client version number not provided")
            return jsonify({"error": "Client version number not provided"}), 400

        return func(*args, **kwargs)

    return validate_version