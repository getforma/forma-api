from app.endpoints.running_sessions import register_running_session_endpoints
from app.endpoints.users import register_user_endpoints

def register_endpoints(app):
    register_running_session_endpoints(app)
    register_user_endpoints(app)