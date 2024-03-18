from code.carly_server import carly_server
import pytest

flask_app = carly_server.app

@pytest.fixture
def app():
    yield flask_app
@pytest.fixture
def client(app):
    return app.test_client()