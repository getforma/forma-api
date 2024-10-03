#import boto3
from flask import request, jsonify
from app.auth import auth_required
from app.config import Config
from uuid import uuid4
#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table(Config.DYNAMODB_TABLE)

def register_endpoints(app):
    @app.route('/', methods=['GET'])
    def index():
        return "hey"

    @app.route('/sessions', methods=['POST'])
    @auth_required
    def create_new_session():
        session_id = str(uuid4())
        return jsonify({"message": f"Running session [{session_id}] started, baby"}), 201

    @app.route('/sessions/:id/track', methods=['POST'])
    @auth_required
    def track_session_data():
        return jsonify({"message": "Tracked data"}), 200

    @app.route('/sessions/:id/end', methods=['POST'])
    @auth_required
    def end_session():
        return jsonify({"message": "Session ended"}), 200
