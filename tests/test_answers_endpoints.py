from tests.test_endpoints import FormaAPIEndpoints
from app.database import db
from app.entities.questionnaire import Questionnaire
from app.entities.question import Question
from app.entities.option import Option
from app.entities.answer import Answer

class TestAnswersEndpoints(FormaAPIEndpoints):
    def tearDown(self):
        """Runs after each test"""
        # Clean up test data
        db.session.query(Answer).delete()
        db.session.query(Option).delete()
        db.session.query(Question).delete()
        db.session.query(Questionnaire).delete()
        super().tearDown()

    def test_create_answer(self):
        """It should record answers for multiple questions"""
        # First create a questionnaire with questions
        questionnaire_data = {
            "name": "Mood Check",
            "key": "mood_check",
            "questions": [
                {
                    "label": "How happy are you?",
                    "question_type": "multiple_choice",
                    "options": [
                        {"label": "Very", "value": 5},
                        {"label": "Somewhat", "value": 3}
                    ]
                },
                {
                    "label": "Energy level?",
                    "question_type": "multiple_choice",
                    "options": [
                        {"label": "High", "value": 5},
                        {"label": "Low", "value": 1}
                    ]
                }
            ]
        }
        
        # Create the questionnaire to get question IDs
        create_resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        created_data = create_resp.get_json()
        questions = created_data['questions']
        
        # Get the options for each question
        q1_options = questions[0]['options']
        q2_options = questions[1]['options']
        
        # Submit answers using option IDs
        answer_data = {
            "running_session_id": "test_session_123",
            "data": [
                {"question_id": questions[0]['id'], "answer_value": q1_options[0]['id']},  # "Very" option
                {"question_id": questions[1]['id'], "answer_value": q2_options[1]['id']}   # "Low" option
            ]
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('message', data)

    def test_create_answer_invalid_questions(self):
        """It should reject answers with invalid question IDs"""
        answer_data = {
            "running_session_id": "test_session_123",
            "data": [
                {"question_id": "invalid_id", "answer_value": 5}
            ]
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

    def test_create_answer_missing_fields(self):
        """It should reject answers with missing required fields"""
        # Missing running_session_id
        answer_data = {
            "data": [
                {"question_id": "some_id", "answer_value": 5}
            ]
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

        # Missing data array
        answer_data = {
            "running_session_id": "test_session_123"
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json()) 

    def test_create_answer_with_multiple_options(self):
        """It should record answers with multiple selected options"""
        # First create a questionnaire with a multiple-select question
        questionnaire_data = {
            "name": "Multiple Choice Test",
            "key": "multiple_choice_test",
            "questions": [
                {
                    "label": "Select all that apply",
                    "question_type": "multiple_select",
                    "options": [
                        {"label": "Option A", "value": 1},
                        {"label": "Option B", "value": 2},
                        {"label": "Option C", "value": 3}
                    ]
                }
            ]
        }
        
        create_resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        created_data = create_resp.get_json()
        question = created_data['questions'][0]
        options = question['options']
        
        # Submit multiple options as answer
        answer_data = {
            "running_session_id": "test_session_123",
            "data": [
                {
                    "question_id": question['id'], 
                    "answer_value": [options[0]['id'], options[1]['id']]  # Select first two options
                }
            ]
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertIn('message', data)

    def test_create_answer_invalid_option_ids(self):
        """It should reject answers with invalid option IDs"""
        # Create a basic questionnaire first
        questionnaire_data = {
            "name": "Test",
            "key": "test",
            "questions": [
                {
                    "label": "Question 1",
                    "question_type": "multiple_choice",
                    "options": [{"label": "Option A", "value": 1}]
                }
            ]
        }
        
        create_resp = self.client.post("/questionnaires", json=questionnaire_data, headers=self.headers)
        created_data = create_resp.get_json()
        question = created_data['questions'][0]
        
        answer_data = {
            "running_session_id": "test_session_123",
            "data": [
                {"question_id": question['id'], "answer_value": "invalid_option_id"}
            ]
        }
        
        resp = self.client.post("/answers", json=answer_data, headers=self.headers)
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json()) 