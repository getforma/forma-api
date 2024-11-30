from unittest import TestCase
from wsgi import app
import json

class TestUserEndpoints(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

    def test_create_user_success(self):
        data = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        response = self.client.post('/users', 
                                  data=json.dumps(data),
                                  headers=self.headers)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['email'], data['email'])
        self.assertEqual(response_data['name'], data['name'])
        self.assertIn('id', response_data)
        self.assertIn('created_at', response_data)
        self.assertIn('updated_at', response_data)

    def test_create_user_missing_fields(self):
        data = {'email': 'test@example.com'}
        response = self.client.post('/users', 
                                  data=json.dumps(data),
                                  headers=self.headers)
        self.assertEqual(response.status_code, 400) 