from flask import request, jsonify
from app.auth import auth_required
from app.entities.running_session import RunningSession
from app.entities.running_session_data import RunningSessionData
from app.utils.running_metrics import *
import time
from app.repositories.running_session_data_repository import RunningSessionDataRepository
import threading
import logging


running_session_data_repo = RunningSessionDataRepository()

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
        logging.info(f"Created running sesssion for {data['user_name']}. ID: {run.id}")
        return jsonify(run.to_dict()), 201

    def insert_data_points(id, raw_data):
        """
        Inserts the new data received from the device into the database in a background thread to not block the API response
        """
        logging.info(f"Inserting {len(raw_data)} data points for session {id}")
        for point in raw_data:
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

    

    @app.route('/sessions/<id>/track', methods=['POST'])
    @auth_required
    def track_session_data(id):
        '''
        Track the session data for a running session.
        This function will:
        - Parse the raw data received from the device into a dataframe
        - Query the existing data for this running session so that we can analyze the whole run
        - Create a "final" dataframe that appends the existing data with the new data received from the device
        - Inserts the new data received from the device into the database in a background thread to not block the API response
        - Calculate the metrics for the entire run using the final concatenated dataframe
        - Return the metrics to the client
        '''
        # start timer to measure time taken to track the session
        start_time = time.time()

        # Parse the raw data received from the device into a dataframe
        raw_data = request.json
        new_df, axis = create_dataframe_and_detect_axis(raw_data)
        logging.info(f"Tracking session data for {id}. Got {len(raw_data)} points")

        # First get existing data and create dataframe
        existing_data = running_session_data_repo.query_data_by_session_id(id)
        logging.info(f"Queried {len(existing_data)} existing points for session {id}")

        final_df = new_df
        
        if existing_data:
            # Create a dataframe from the existing data and concatenate it with the new dataframe
            df_existing = create_dataframe_from_dynamo_data(existing_data)
            final_df = pd.concat([df_existing, new_df], ignore_index=True)
            
        # Clean and detect the axis of the running session
        axis = detect_up_down_axis(final_df)
        final_df = final_clean_data(final_df, axis)
        logging.info(f"Final dataframe has {len(final_df)} points")

        # Start background thread for data insertion
        insert_thread = threading.Thread(target=insert_data_points, args=(id, raw_data))
        insert_thread.start()

        # Calculate metrics and return response
        response_body = calculate_session_metrics(final_df, axis)
        end_time = time.time()
        logging.info(f"Calculated metrics in {end_time - start_time} seconds")
        response_body["time_taken"] = end_time - start_time
        return jsonify(response_body), 201

    @app.route('/sessions/<id>/analyze', methods=['POST'])
    @auth_required
    def analyze_session(id):
        # start timer to measure time taken to analyze the split
        start_time = time.time()

        # Get start and end time from request body
        request_data = request.get_json()
        split_start_time = request_data.get('start_time')
        split_end_time = request_data.get('end_time')

        if not split_start_time or not split_end_time:
            return jsonify({'error': 'start_time and end_time are required'}), 400
        
        split_data = running_session_data_repo.query_data_by_session_id_and_time_range(id, split_start_time, split_end_time)
        final_df = create_dataframe_from_dynamo_data(split_data)
        axis = detect_up_down_axis(final_df)
        final_df = final_clean_data(final_df, axis)

        logging.info(f"Analyzing split with {len(final_df)} points")
        # Calculate metrics
        response_body = calculate_session_metrics(final_df, axis)
        
        # Measure time taken
        end_time = time.time()
        logging.info(f"Calculated metrics in {end_time - start_time} seconds")
        response_body["total_data_points"] = len(final_df)
        response_body["time_taken"] = end_time - start_time
        
        return jsonify(response_body), 200