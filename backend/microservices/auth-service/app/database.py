# app/database.py - Configuração do SQLite
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    # Configuração do SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_service.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Cria tabelas se não existirem
    with app.app_context():
        db.create_all()