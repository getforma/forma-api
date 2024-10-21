from flask import request, jsonify
from app.auth import auth_required
from app.entities.running_session import RunningSession
from app.entities.running_session_data import RunningSessionData
from app.utils.running_metrics import *

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

        ##############################################
        # TODO :Calculate metrics
        ##############################################
        distance = calculate_distance(data)
        speed = calculate_speed(data)
        cadence = calculate_cadence(data)
        vertical_oscillation = calculate_vertical_oscillation(data)
        stride_length = calculate_stride_length(data)
        ground_contact_time = calculate_ground_contact_time(data)
        pace = calculate_pace(data)
        return jsonify({
            "start_time": data[0]['time'],
            "end_time": data[-1]['time'],
            "distance": distance,
            "speed": speed,
            "cadence": cadence,
            "vertical_oscillation": vertical_oscillation,
            "stride_length": stride_length,
            "ground_contact_time": ground_contact_time,
            "pace": pace
        }), 201
