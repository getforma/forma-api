from flask import request, jsonify
from app.auth.jwt_decoder import jwt_required
from app.entities.question import Question
from app.entities.option import Option
from app.database import db
from http import HTTPStatus

def register_question_endpoints(app):
    @app.route('/questions', methods=['POST'])
    @jwt_required
    def create_question():
        data = request.get_json()
        
        if not data or not data.get('question_text') or not data.get('question_type'):
            return jsonify({'error': 'Question text and type are required'}), HTTPStatus.BAD_REQUEST
            
        if not data.get('options') or not isinstance(data['options'], list):
            return jsonify({'error': 'Options array is required'}), HTTPStatus.BAD_REQUEST
            
        try:
            question = Question(
                question_text=data['question_text'],
                question_type=data['question_type']
            )
            db.session.add(question)
            
            for option_data in data['options']:
                if not option_data.get('option_text') or not option_data.get('option_value'):
                    return jsonify({'error': 'Option text is required for all options'}), HTTPStatus.BAD_REQUEST
                    
                option = Option(
                    option_text=option_data['option_text'],
                    option_value=option_data['option_value'],
                    question=question
                )
                db.session.add(option)
                
            db.session.commit()
            
            return jsonify(question.to_dict()), HTTPStatus.CREATED
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/questions', methods=['GET'])
    @jwt_required
    def get_questions():
        questions = Question.query.all()
        return jsonify([{
            'id': question.id,
            'question_text': question.question_text,
            'question_type': question.question_type,
            'options': [option.to_dict_minimal() for option in question.options]
        } for question in questions]), HTTPStatus.OK