from flask import request, abort
from functools import wraps
from app.config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != Config.BASIC_AUTH_USERNAME or auth.password != Config.BASIC_AUTH_PASSWORD:
            return abort(401, 'Authentication required')
        return f(*args, **kwargs)
    return decorated
