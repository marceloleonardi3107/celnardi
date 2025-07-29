from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos usando strings
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'order_index': self.order_index,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'lessons_count': len(self.lessons)
        }

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    order_index = db.Column(db.Integer, nullable=False)
    lesson_type = db.Column(db.String(50), default='text')  # text, video, audio, pdf
    media_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos usando strings para evitar problemas de importação circular
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True, cascade='all, delete-orphan')
    media_files = db.relationship('MediaFile', backref='lesson', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'content': self.content,
            'order_index': self.order_index,
            'lesson_type': self.lesson_type,
            'media_url': self.media_url,
            'duration_minutes': self.duration_minutes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'has_quiz': len(self.quizzes) > 0
        }

class MediaFile(db.Model):
    __tablename__ = 'media_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # video, audio, image, pdf
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'lesson_id': self.lesson_id,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

