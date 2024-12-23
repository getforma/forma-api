import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv('FLASK_ENV', 'production')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    RUNNING_SESSIONS_TABLE = os.getenv('RUNNING_SESSIONS_TABLE', 'forma-running-sessions')
    RUNNING_SESSIONS_DATA_TABLE = os.getenv('RUNNING_SESSIONS_DATA_TABLE', 'forma-running-sessions-data')
    BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'password')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Use different database URLs based on environment
    database_url = os.getenv('TEST_DATABASE_URL' if ENV == 'test' else 'DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def is_test(cls):
        return cls.ENV == 'test'
