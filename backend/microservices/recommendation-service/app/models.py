# app/models.py - Modelos do Recommendation Service
from .database import db
from datetime import datetime, timezone

class LearningMaterial(db.Model):
    __tablename__ = 'learning_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(500))  # Tags como string separada por vírgulas
    type = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(10))
    pages = db.Column(db.Integer)
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'tags': self.tags.split(',') if self.tags else [],
            'type': self.type,
            'difficulty': self.difficulty,
            'area': self.area,
            'nivel': self.nivel,
            'description': self.description,
            'image': self.image,
            'pages': self.pages,
            'year': self.year
        }

class UserHistory(db.Model):
    __tablename__ = 'user_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    areas = db.Column(db.String(500))  # Áreas como string separada por vírgulas
    nivel = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


###nova classe
class UserBookList(db.Model):
    __tablename__ = 'user_book_lists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('learning_materials.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(50), default='quero_ler')  # quero_ler, lendo, lido
    
    # Relacionamento com o material
    material = db.relationship('LearningMaterial', backref='user_lists')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'material_id': self.material_id,
            'material': self.material.to_dict() if self.material else None,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'status': self.status
        }