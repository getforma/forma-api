from app.database import db
from datetime import datetime
from uuid import uuid4

class Questionnaire(db.Model):
    __tablename__ = 'questionnaires'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    questions = db.relationship('Question', backref='questionnaire', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'questions': [question.to_dict() for question in self.questions]
        } 

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'questions': [question.serialize() for question in self.questions]
        }
