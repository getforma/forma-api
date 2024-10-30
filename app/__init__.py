from flask import Flask
from app.config import Config
from app.auth import auth_required
from app.endpoints import register_endpoints
import logging

def create_app():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    register_endpoints(app)

    return app
