from app.database import db
from datetime import datetime
from uuid import uuid4

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    label = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    options = db.relationship('Option', backref='question', lazy=True)
    sort_index = db.Column(db.Integer, nullable=True)
    question_type = db.Column(db.String(255), nullable=True, default='multiple_choice')
    questionnaire_id = db.Column(db.String(36), db.ForeignKey('questionnaires.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'options': [option.to_dict() for option in self.options],
            'question_type': self.question_type,
            'questionnaire_id': self.questionnaire_id,
            'sort_index': self.sort_index
        } 
    
    def serialize(self):
        return {
            'id': self.id,
            'sort_index': self.sort_index,
            'question_type': self.question_type,
            'label': self.label,
            'options': [option.serialize() for option in self.options],
            
        }
