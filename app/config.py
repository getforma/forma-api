import os

class Config:
    DEBUG = os.getenv('FLASK_DEBUG', False)
    RUNNING_SESSIONS_TABLE = os.getenv('RUNNING_SESSIONS_TABLE', 'forma-running-sessions')
    RUNNING_SESSIONS_DATA_TABLE = os.getenv('RUNNING_SESSIONS_DATA_TABLE', 'forma-running-sessions-data')
    BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME', 'admin')
    BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'password')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
