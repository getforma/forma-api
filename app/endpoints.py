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
        print(f"===============> Created running sesssion for {data['user_name']}. ID: {run.id}")
        return jsonify(run.to_dict()), 201

    @app.route('/sessions/<id>/track', methods=['POST'])
    @auth_required
    def track_session_data(id):
        data = request.json
        print(f"===============> Tracking session data for {id}. Got {len(data)} points")
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
        print(f"===============> Created {len(data)} points for session {id}")
        #create dataframe and clean data
        df, axis = create_dataframe_and_detect_axis(data)

        distance = calculate_distance(df)
        speed = calculate_speed(df, distance)
        pace = calculate_pace(df, speed)
        cadence = calculate_cadence(df, axis)
        vertical_oscillation = calculate_vertical_oscillation(df, axis)
        stride_length = calculate_stride_length(df, axis, speed)
        ground_contact_time = calculate_ground_contact_time(df, axis)
        print(f"===============> Calculated metrics for session {id}")
        print({
            "start_time": data[0]['time'],
            "end_time": data[-1]['time'],
            "distance": distance,
            "speed": speed,
            "pace": pace,
            "cadence": cadence,
            "vertical_oscillation": vertical_oscillation,
            "stride_length": stride_length,
            "ground_contact_time": ground_contact_time,
        })
        return jsonify({
            "start_time": data[0]['time'],
            "end_time": data[-1]['time'],
            "distance": distance,
            "speed": speed,
            "pace": pace,
            "cadence": cadence,
            "vertical_oscillation": vertical_oscillation,
            "stride_length": stride_length,
            "ground_contact_time": ground_contact_time,
        }), 201
