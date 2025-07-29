from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    status = db.Column(db.String(50), default='not_started')  # not_started, in_progress, completed
    progress_percentage = db.Column(db.Float, default=0.0)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    last_accessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent_minutes = db.Column(db.Integer, default=0)
    
    # Índices únicos para evitar duplicatas
    __table_args__ = (
        db.UniqueConstraint('user_id', 'module_id', 'lesson_id', name='unique_user_lesson_progress'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'lesson_id': self.lesson_id,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'last_accessed_at': self.last_accessed_at.isoformat() if self.last_accessed_at else None,
            'time_spent_minutes': self.time_spent_minutes
        }

class UserCertificate(db.Model):
    __tablename__ = 'user_certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    certificate_code = db.Column(db.String(100), unique=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    final_score = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'certificate_code': self.certificate_code,
            'issued_at': self.issued_at.isoformat() if self.issued_at else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'final_score': self.final_score
        }

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # login, lesson_start, lesson_complete, quiz_attempt
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=True)
    details = db.Column(db.Text)  # JSON string com detalhes adicionais
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'activity_type': self.activity_type,
            'module_id': self.module_id,
            'lesson_id': self.lesson_id,
            'quiz_id': self.quiz_id,
            'details': self.details,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

