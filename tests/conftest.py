import os

def pytest_configure(config):
    os.environ['FLASK_ENV'] = 'test'