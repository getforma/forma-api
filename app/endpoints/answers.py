from flask import request, jsonify
from app.auth.jwt_decoder import jwt_required
from app.entities.question import Question
from app.entities.answer import Answer
from app.entities.option import Option
from app.database import db
from http import HTTPStatus

def register_answers_endpoints(app):
    @app.route('/answers', methods=['POST'])
    @jwt_required
    def create_answer():
        data = request.get_json()
        if not data or not data.get('running_session_id') or not data.get('data'):
            return jsonify({'error': 'running_session_id and data are required'}), HTTPStatus.BAD_REQUEST
            
        if not isinstance(data['data'], list):
            return jsonify({'error': 'data must be an array'}), HTTPStatus.BAD_REQUEST
            
        try:
            # Validate all question IDs and option IDs
            question_ids = {str(answer['question_id']) for answer in data['data']}
            questions = Question.query.filter(
                Question.id.in_(question_ids)
            ).all()
            
            if len(questions) != len(question_ids):
                return jsonify({'error': 'Invalid question IDs provided'}), HTTPStatus.BAD_REQUEST
            
            # Collect and validate all option IDs
            all_option_ids = set()
            for answer_data in data['data']:
                option_ids = answer_data['answer_value']
                if isinstance(option_ids, str):
                    all_option_ids.add(option_ids)
                elif isinstance(option_ids, list):
                    all_option_ids.update(option_ids)
                else:
                    return jsonify({'error': 'answer_value must be an option ID or array of option IDs'}), HTTPStatus.BAD_REQUEST
            
            # Verify options exist and belong to the correct questions
            options = Option.query.filter(Option.id.in_(all_option_ids)).all()
            if len(options) != len(all_option_ids):
                return jsonify({'error': 'Invalid option IDs provided'}), HTTPStatus.BAD_REQUEST
            
            # Create answer records
            for answer_data in data['data']:
                option_ids = answer_data['answer_value']
                ids = option_ids if isinstance(option_ids, list) else [option_ids]
                
                for option_id in ids:
                    answer = Answer(
                        user_id=request.user.id,
                        question_id=answer_data['question_id'],
                        running_session_id=data['running_session_id'],
                        option_id=option_id
                    )
                    db.session.add(answer)
                
            db.session.commit()
            return jsonify({'message': 'Answers recorded successfully', 'score': 42}), HTTPStatus.CREATED
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    