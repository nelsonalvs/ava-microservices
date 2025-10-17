# app/models.py - Modelos do banco de dados
from .database import db
from datetime import datetime, timezone
import jwt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def generate_token(self):
        """Gera token JWT para o usuário"""
        from datetime import datetime, timezone, timedelta
        
        payload = {
            'user_id': self.id,
            'username': self.username,
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }
        return jwt.encode(payload, 'ava_secret_key_2024', algorithm='HS256')