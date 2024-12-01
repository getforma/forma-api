from app.database import db
from datetime import datetime
from uuid import uuid4

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    value = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    running_session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'running_session_id': self.running_session_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
    
    def serialize(self):
        return {
            'id': self.id,
            'value': self.value,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'running_session_id': self.running_session_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
