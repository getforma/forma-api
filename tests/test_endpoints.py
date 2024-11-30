import logging
from unittest import TestCase
from wsgi import app
import uuid
from tests.mock_data import *
from app.database import db
from app.entities.user import User

class FormaAPIEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

        # Create all database tables
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        
        # Create test user for each test
        self.test_user = User(
            email="test@example.com",
            name="Test User"
        )
        db.session.add(self.test_user)
        db.session.commit()
        
        # Create headers with matching email in token
        self.headers = auth_headers(email="test@example.com")

    def tearDown(self):
        """Runs after each test"""
        # Clean up test user
        db.session.query(User).delete()
        db.session.commit()

    def _create_session(self):
        """Helper method to create a session and return its data"""
        body = create_session_body()
        resp = self.client.post("/sessions", json=body, headers=self.headers)
        if resp.status_code != 201:
            print(f"Response data: {resp.data}")
        self.assertEqual(resp.status_code, 201)
        return resp.get_json(), body, self.headers

    def _validate_session_data(self, data, body):
        """Helper method to validate session response data"""
        required_fields = ['created_at', 'id', 'device_id', 'device_position', 'user_name']
        for field in required_fields:
            self.assertIn(field, data)
        
        self.assertEqual(data['device_id'], body['device_id'])
        self.assertEqual(data['device_position'], body['device_position']) 
        
        try:
            uuid.UUID(data['id'])
        except ValueError:
            self.fail("id is not a valid UUID")

    def _validate_tracking_data(self, data):
        """Helper method to validate tracking response data"""
        expected_fields = [
            'start_time', 'end_time', 'distance', 'speed', 'pace', 
            'cadence', 'vertical_oscillation', 'stride_length', 
            'ground_contact_time', 'time_taken', 'total_datapoints'
        ]
        
        # Validate presence of fields
        for field in expected_fields:
            self.assertIn(field, data)
        
        # Validate types
        self.assertIsInstance(data['start_time'], str)
        self.assertIsInstance(data['end_time'], str)
        numeric_fields = ['distance', 'speed', 'pace', 'cadence', 
                         'vertical_oscillation', 'stride_length', 
                         'ground_contact_time', 'time_taken']
        for field in numeric_fields:
            self.assertIsInstance(data[field], (int, float))
        self.assertIsInstance(data['total_datapoints'], int)

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        response = str(resp.data.decode("utf-8"))
        self.assertIn("Forma API v0.1.0", response)

    def test_create_running_session(self):
        """It should create a running session"""
        data, body, _ = self._create_session()
        self._validate_session_data(data, body)
    
    def test_track_running_session(self):
        """It should track a running session"""
        session_data, _, headers = self._create_session()
        track_body = track_session_body()
        resp = self.client.post(
            f"/sessions/{session_data['id']}/track", 
            json=track_body, 
            headers=headers
        )
        self.assertEqual(resp.status_code, 201)
        self._validate_tracking_data(resp.get_json())

    def test_track_running_session_multiple_times(self):
        """It should track a running session multiple times"""
        session_data, _, headers = self._create_session()
        session_id = session_data['id']

        # First tracking
        resp = self.client.post(
            f"/sessions/{session_id}/track", 
            json=track_session_body(), 
            headers=headers
        )
        self.assertEqual(resp.get_json()['total_datapoints'], 9)

        # Second tracking
        resp = self.client.post(
            f"/sessions/{session_id}/track", 
            json=additional_track_session_body(), 
            headers=headers
        )
        self.assertEqual(resp.get_json()['total_datapoints'], 18)