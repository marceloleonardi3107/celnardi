from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    
    # Campos específicos para o sistema de treinamento
    full_name = db.Column(db.String(200))
    department = db.Column(db.String(100))  # vendas, suporte, gerencia, etc
    position = db.Column(db.String(100))    # consultor, supervisor, gerente, etc
    hire_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    profile_picture = db.Column(db.String(500))
    
    # Status e controle
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    progress = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True, cascade='all, delete-orphan')
    certificates = db.relationship('UserCertificate', backref='user', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('UserActivity', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Define a senha do usuário com hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_sensitive=False):
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'department': self.department,
            'position': self.position,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'phone': self.phone,
            'profile_picture': self.profile_picture,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            result['password_hash'] = self.password_hash
            
        return result
