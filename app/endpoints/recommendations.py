from flask import request, jsonify
from app.auth.jwt_decoder import jwt_required
from app.entities.user import User
from http import HTTPStatus
from datetime import datetime, timedelta

def create_recommendations(susceptibility_score):
    today = datetime.now()
    
    if susceptibility_score < 20:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "long"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "intervals"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "easy"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "tempo"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "hills"
            }
        ]
    elif 20 <= susceptibility_score < 40:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "moderate"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "cross"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "easy"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "fartlek"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "strength"
            }
        ]
    elif 40 <= susceptibility_score < 60:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "easy"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "cross"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "recovery"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "mobility"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "easy"
            }
        ]
    elif 60 <= susceptibility_score < 80:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "recovery"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "mobility"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "cross"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "recovery"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "mobility"
            }
        ]
    elif 80 <= susceptibility_score < 95:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "recovery"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "mobility"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "recovery"
            }
        ]
    else:
        return [
            {
                "date": (today - timedelta(hours=4) + timedelta(days=0)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=1)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=2)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=3)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            },
            {
                "date": (today - timedelta(hours=4) + timedelta(days=4)).strftime("%Y/%m/%d"),
                "trainingType": "rest"
            }
        ]

def register_recommendations_endpoints(app):
    @app.route('/recommendation', methods=['GET'])
    @jwt_required
    def get_recommendations():
        user_id = request.user.id
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), HTTPStatus.NOT_FOUND
        
        recommendations = create_recommendations(user.susceptibility_score)
        return jsonify(recommendations), HTTPStatus.OK
        
    