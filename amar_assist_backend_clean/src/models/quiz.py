from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    passing_score = db.Column(db.Integer, default=70)  # Porcentagem mínima para aprovação
    max_attempts = db.Column(db.Integer, default=3)
    time_limit_minutes = db.Column(db.Integer, default=30)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'title': self.title,
            'description': self.description,
            'passing_score': self.passing_score,
            'max_attempts': self.max_attempts,
            'time_limit_minutes': self.time_limit_minutes,
            'is_active': self.is_active,
            'questions_count': len(self.questions),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # multiple_choice, true_false, text
    options = db.Column(db.Text)  # JSON string para opções de múltipla escolha
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)  # Explicação da resposta correta
    points = db.Column(db.Integer, default=1)
    order_index = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_options(self):
        """Retorna as opções como lista Python"""
        if self.options:
            try:
                return json.loads(self.options)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_options(self, options_list):
        """Define as opções a partir de uma lista Python"""
        self.options = json.dumps(options_list, ensure_ascii=False)
    
    def to_dict(self, include_correct_answer=False):
        result = {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.get_options(),
            'points': self.points,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_correct_answer:
            result['correct_answer'] = self.correct_answer
            result['explanation'] = self.explanation
            
        return result

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float)  # Pontuação obtida
    max_score = db.Column(db.Float)  # Pontuação máxima possível
    percentage = db.Column(db.Float)  # Porcentagem de acerto
    passed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    time_taken_minutes = db.Column(db.Integer)
    
    # Relacionamentos
    answers = db.relationship('QuizAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': self.percentage,
            'passed': self.passed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'time_taken_minutes': self.time_taken_minutes
        }

class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Float, default=0)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'attempt_id': self.attempt_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct,
            'points_earned': self.points_earned,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None
        }

