import logging
import os
from unittest import TestCase
from wsgi import app
import uuid
from tests.mock_data import *
from app.config import Config
class FormaAPIEndpoints(TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

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