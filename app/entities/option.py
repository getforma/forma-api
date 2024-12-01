from app.database import db
from datetime import datetime
from uuid import uuid4

class Option(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    label = db.Column(db.String(255), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey('questions.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label, 
            'value': self.value,
            'question_id': self.question_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 
    def to_dict_minimal(self):
        return {
            'id': self.id,
            'label': self.label, 
            'value': self.value,
        } 
    
    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
        }   