import logging
from unittest import TestCase
from wsgi import app
from moto import mock_aws
import uuid
from tests.mock_data import *
from tests.setup_dynamo_mock import setup_dynamo_mock
class FormaAPIEndpoints(TestCase):
    @classmethod
    @mock_aws
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()
        
        # Create mock DynamoDB tables
        setup_dynamo_mock()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        response = str(resp.data.decode("utf-8"))
        self.assertIn("Forma API v0.1.0", response)

    def test_create_running_session(self):
        """It should create a running session"""
        body = create_session_body()
        headers = auth_headers()
        resp = self.client.post("/sessions", json=body, headers=headers)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('created_at', data)
        self.assertIn('id', data)
        self.assertIn('device_id', data)
        self.assertIn('device_position', data)
        self.assertIn('user_name', data)
        self.assertEqual(data['device_id'], body['device_id'])
        self.assertEqual(data['device_position'], body['device_position']) 
        self.assertEqual(data['user_name'], body['user_name'])
        try:
            uuid.UUID(data['id'])
        except ValueError:
            self.fail("id is not a valid UUID")