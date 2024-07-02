import sys
import os
import pytest

# Add the root directory (two levels up) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from server import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def client_with_user(app):
    with app.test_client() as client:
        with app.test_request_context():
            # Modify the session directly
            from flask import session
            session["user_email"] = "rotana12@gmail.com"
        yield client