from tests.test_endpoints import FormaAPIEndpoints
from app.database import db
from app.entities.questionnaire import Questionnaire
from app.entities.question import Question
from app.entities.option import Option

class TestQuestionnaireEndpoints(FormaAPIEndpoints):
    def tearDown(self):
        """Runs after each test"""
        # Clean up test data
        db.session.query(Option).delete()
        db.session.query(Question).delete()
        db.session.query(Questionnaire).delete()
        super().tearDown()  # Clean up user from parent class

    def test_create_questionnaire(self):
        """It should create a questionnaire with questions and options"""
        questionnaire_data = {
            "name": "Daily Mood Check",
            "key": "daily_mood",
            "questions": [
                {
                    "label": "How do you feel today?",
                    "options": [
                        {"label": "Great", "value": 5},
                        {"label": "Good", "value": 4},
                        {"label": "Okay", "value": 3}
                    ]
                },
                {
                    "label": "Energy level?",
                    "options": [
                        {"label": "High", "value": 3},
                        {"label": "Medium", "value": 2},
                        {"label": "Low", "value": 1}
                    ]
                }
            ]
        }

        resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        
        data = resp.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], questionnaire_data['name'])
        self.assertEqual(data['key'], questionnaire_data['key'])
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(len(data['questions'][0]['options']), 3)

    def test_create_questionnaire_missing_fields(self):
        """It should return 400 when required fields are missing"""
        # Missing name
        questionnaire_data = {
            "key": "daily_mood",
            "questions": [
                {
                    "label": "How do you feel today?",
                    "options": [{"label": "Great", "value": 5}]
                }
            ]
        }
        
        resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_get_questionnaire(self):
        """It should return a questionnaire by key or id"""
        # First create a questionnaire
        questionnaire_data = {
            "name": "Daily Check",
            "key": "daily_check",
            "questions": [
                {
                    "label": "Sleep quality?",
                    "options": [
                        {"label": "Good", "value": 3},
                        {"label": "Poor", "value": 1}
                    ]
                }
            ]
        }
        
        create_resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        created_data = create_resp.get_json()
        
        # Test getting by key
        resp = self.client.get(f"/questionnaires/daily_check", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['name'], questionnaire_data['name'])
        self.assertEqual(len(data['questions']), 1)
        
        # Test getting by id
        resp = self.client.get(f"/questionnaires/{created_data['id']}", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['id'], created_data['id'])

    def test_get_nonexistent_questionnaire(self):
        """It should return 404 for non-existent questionnaire"""
        resp = self.client.get("/questionnaires/nonexistent", headers=self.headers)
        self.assertEqual(resp.status_code, 404)

    def test_questions_sort_order(self):
        """It should maintain question sort order"""
        questionnaire_data = {
            "name": "Ordered Questions",
            "key": "ordered",
            "questions": [
                {"label": "Question 1", "options": [{"label": "Yes", "value": 1}]},
                {"label": "Question 2", "options": [{"label": "Yes", "value": 1}]},
                {"label": "Question 3", "options": [{"label": "Yes", "value": 1}]}
            ]
        }
        
        create_resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        self.assertEqual(create_resp.status_code, 201)
        
        # Get the questionnaire and verify order
        resp = self.client.get("/questionnaires/ordered", headers=self.headers)
        data = resp.get_json()
        
        questions = data['questions']
        self.assertEqual(len(questions), 3)
        self.assertEqual(questions[0]['sort_index'], 0)
        self.assertEqual(questions[1]['sort_index'], 1)
        self.assertEqual(questions[2]['sort_index'], 2)
