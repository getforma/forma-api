from app.endpoints.running_sessions import register_running_session_endpoints
from app.endpoints.users import register_user_endpoints
from app.endpoints.questions import register_question_endpoints
from app.endpoints.questionnaire import register_questionnaire_endpoints
from app.endpoints.answers import register_answers_endpoints
from app.endpoints.recommendations import register_recommendations_endpoints

def register_endpoints(app):
    register_running_session_endpoints(app)
    register_user_endpoints(app)
    register_question_endpoints(app)
    register_questionnaire_endpoints(app)
    register_answers_endpoints(app)
    register_recommendations_endpoints(app)