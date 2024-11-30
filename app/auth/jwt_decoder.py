from functools import wraps
from flask import request, abort, current_app
import jwt
from app.entities.user import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return abort(401, 'No token provided')
        token = auth_header.split('Bearer ')[1]
        try:
            # Decode token without verification
            payload = jwt.decode(token, options={"verify_signature": False})
            # Get email from token
            email = payload.get('email')
            if not email:
                return abort(401, 'Invalid token: no email claim')
            # Find user in database
            user = User.query.filter_by(email=email).first()
            
            if not user:
                return abort(401, 'User not found')
            
            # Add user to request context
            request.user = user
            return f(*args, **kwargs)
            
        except jwt.InvalidTokenError as e:
            return abort(401, f'Invalid token: {str(e)}')
            
    return decorated 