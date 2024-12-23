from app.database import db
from datetime import datetime
from uuid import uuid4

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    option_id = db.Column(db.String(36), db.ForeignKey('options.id'), nullable=True)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    running_session_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Add relationships
    option = db.relationship('Option', backref='answers')
    question = db.relationship('Question', backref='answers')

    def to_dict(self):
        return {
            'id': self.id,
            'option_id': self.option_id,
            'option_value': self.option.value if self.option else None,
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
            'option_id': self.option_id,
            'question_id': self.question_id,
            'user_id': self.user_id,
            'running_session_id': self.running_session_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
