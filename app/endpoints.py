from flask import request, jsonify
from app.auth import auth_required
from app.entities.running_session import RunningSession
from app.entities.running_session_data import RunningSessionData
def register_endpoints(app):
    @app.route('/', methods=['GET'])
    def index():
        return "Forma API v0.1.0"

    @app.route('/sessions', methods=['POST'])
    @auth_required
    def create_new_session():
        data = request.json
        run = RunningSession(
            device_id=data['device_id'],
            device_position=data['device_position'],
            user_name=data['user_name']
        )
        return jsonify(run.to_dict()), 201

    @app.route('/sessions/<id>/track', methods=['POST'])
    @auth_required
    def track_session_data(id):
        data = request.json
        for point in data:
            RunningSessionData(
                running_session_id=id,
                time=point['time'],
                lat=point['latitude'],
                long=point['longitude'],
                acceleration=point['acceleration'],
                angular_velocity=point['angular_velocity'],
                magnetic_field=point['magnetic_field'],
                angle=point['angle']
            )

        return jsonify({"ok": True}), 201
