from flask import request, jsonify
from app.entities.user import User
from app.database import db
from http import HTTPStatus

def register_user_endpoints(app):
    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('name'):
            return jsonify({'error': 'Email and name are required'}), HTTPStatus.BAD_REQUEST
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), HTTPStatus.CONFLICT
            
        try:
            user = User(
                email=data['email'],
                name=data['name']
            )
            db.session.add(user)
            db.session.commit()
            
            return jsonify(user.to_dict()), HTTPStatus.CREATED
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR 