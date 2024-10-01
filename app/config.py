import os

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', False)
    DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE', 'forma-running-sessions')
    BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'password')
