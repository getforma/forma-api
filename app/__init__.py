from flask import Flask
from app.config import Config
from app.database import init_db, db
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

    # Initialize database
    init_db(app)

    # Register routes - import here to avoid circular imports
    from app.endpoints import register_endpoints
    register_endpoints(app)

    return app
