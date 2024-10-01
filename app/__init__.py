from flask import Flask
from app.config import Config
from app.auth import auth_required
from app.endpoints import register_endpoints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    register_endpoints(app)

    return app
