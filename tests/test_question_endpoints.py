from tests.test_endpoints import FormaAPIEndpoints
from app.database import db
from app.entities.question import Question
from app.entities.option import Option

class TestQuestionEndpoints(FormaAPIEndpoints):
    def tearDown(self):
        """Runs after each test"""
        # Clean up test data
        db.session.query(Option).delete()
        db.session.query(Question).delete()
        super().tearDown()  # Clean up user from parent class

    def test_create_question(self):
        """It should create a question with options"""
        question_data = {
            "question_text": "How do you feel?",
            "question_type": "mood",
            "options": [
                {"option_text": "Great", "option_value": "5"},
                {"option_text": "Good", "option_value": "4"},
                {"option_text": "Okay", "option_value": "3"}
            ]
        }

        resp = self.client.post("/questions", json=question_data, headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        
        data = resp.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['question_text'], question_data['question_text'])
        self.assertEqual(data['question_type'], question_data['question_type'])
        self.assertEqual(len(data['options']), 3)

    def test_create_question_missing_fields(self):
        """It should return 400 when required fields are missing"""
        # Missing question_text
        question_data = {
            "question_type": "mood",
            "options": [{"option_text": "Great", "option_value": "5"}]
        }
        
        resp = self.client.post("/questions", json=question_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)

    def test_get_questions(self):
        """It should return all questions"""
        # Create a test question first
        question_data = {
            "question_text": "Rate your energy level",
            "question_type": "energy",
            "options": [
                {"option_text": "High", "option_value": "3"},
                {"option_text": "Low", "option_value": "1"}
            ]
        }
        
        # Create the question
        self.client.post("/questions", json=question_data, headers=self.headers)
        
        # Get all questions
        resp = self.client.get("/questions", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['question_text'], question_data['question_text'])
        self.assertEqual(len(data[0]['options']), 2)
