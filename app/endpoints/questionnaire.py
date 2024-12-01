from flask import request, jsonify
from app.auth.jwt_decoder import jwt_required
from app.entities.question import Question
from app.entities.questionnaire import Questionnaire
from app.entities.option import Option
from app.database import db
from http import HTTPStatus

def register_questionnaire_endpoints(app):
    @app.route('/questionnaires', methods=['POST'])
    @jwt_required
    def create_questionnaire():
        data = request.get_json()
        if not data or not data.get('name') or not data.get('key'):
            return jsonify({'error': 'Name and key are required'}), HTTPStatus.BAD_REQUEST
            
        if not data.get('questions') or not isinstance(data['questions'], list):
            return jsonify({'error': 'Questions array is required'}), HTTPStatus.BAD_REQUEST
            
        try:
            questionnaire = Questionnaire(
                name=data['name'],
                key=data['key']
            )
            db.session.add(questionnaire)
            for i, question_data in enumerate(data['questions']):
                if not question_data.get('label'):
                    return jsonify({'error': 'Label is required for all questions'}), HTTPStatus.BAD_REQUEST
                    
                question = Question(
                    label=question_data['label'],
                    questionnaire=questionnaire,
                    sort_index=i,
                )
                db.session.add(question)

                for option_data in question_data.get('options', []):
                    print("===========option_data", option_data)
                    if not option_data.get('label') or not option_data.get('value'):
                        print("===========option label", option_data.get('label'))
                        print("===========option value", option_data.get('value'))
                        return jsonify({'error': 'Label and value are required for all options'}), HTTPStatus.BAD_REQUEST
                        
                    option = Option(
                        label=option_data['label'],
                        value=option_data['value'],
                        question=question
                    )
                    db.session.add(option)
                
            db.session.commit()
            
            return jsonify(questionnaire.to_dict()), HTTPStatus.CREATED
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        
    @app.route('/questionnaires/<string:key>', methods=['GET'])
    @jwt_required
    def get_questionnaire(key):
        questionnaire = Questionnaire.query.filter(
            (Questionnaire.id == key) | (Questionnaire.key == key)
        ).first()
        
        if not questionnaire:
            return jsonify({'error': 'Questionnaire not found'}), HTTPStatus.NOT_FOUND
        
        questionnaire_dict = questionnaire.serialize()  
        questionnaire_dict['questions'] = sorted(questionnaire_dict['questions'], key=lambda x: x['sort_index'])
            
        return jsonify(questionnaire_dict)