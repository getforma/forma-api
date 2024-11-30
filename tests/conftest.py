import os
import pytest
from app import create_app
from app.database import db

@pytest.fixture(autouse=True)
def app():
    # Set test environment
    os.environ['FLASK_ENV'] = 'test'
    
    # Create app with test config
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        yield app
        # Clean up after test
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()