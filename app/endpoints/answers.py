from flask import request, jsonify
from app.auth.jwt_decoder import jwt_required
from app.entities.question import Question
from app.entities.answer import Answer
from app.entities.option import Option
from app.database import db
from http import HTTPStatus

def calculate_susceptibility_score(answers_by_question):
    """Calculate susceptibility score based on answers"""
    total_score = 0
    max_total_weighted_score = 0

    for question_id, answers in answers_by_question.items():
        question = answers[0].question  # Get the question from any answer
        if question.weight:  # Only calculate for questions with weights
            if question.is_summable:
                # Sum values for questions like body parts
                answer_value = sum(answer.option.value for answer in answers)
            else:
                # Use single answer value for other questions
                answer_value = answers[0].option.value

            total_score += question.weight * answer_value
            max_total_weighted_score += question.weight * question.max_score

    if max_total_weighted_score == 0:
        return 0
        
    susceptibility_score = (total_score / max_total_weighted_score) * 100
    return int(round(susceptibility_score))

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
            new_answers = []
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
                    new_answers.append(answer)
                
            db.session.commit()

            # Group answers by question for score calculation
            answers_by_question = {}
            for answer in new_answers:
                if answer.question_id not in answers_by_question:
                    answers_by_question[answer.question_id] = []
                answers_by_question[answer.question_id].append(answer)

            # Calculate score
            score = calculate_susceptibility_score(answers_by_question)
            
            return jsonify({
                'message': 'Answers recorded successfully', 
                'score': score
            }), HTTPStatus.CREATED
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    