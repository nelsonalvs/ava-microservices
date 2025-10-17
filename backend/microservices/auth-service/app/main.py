from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import db, init_db
from .models import User
import bcrypt
from datetime import datetime 
from datetime import datetime, timezone


app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados
init_db(app)

def hash_password(password):
    """Gera hash da senha usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """Verifica se a senha corresponde ao hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

@app.route('/')
def home():
    return jsonify({'message': 'Auth Service com SQLite está rodando!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'SQLite'})

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
        
        # Verifica se usuário já existe
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Usuário já existe!'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email já cadastrado!'}), 400
        
        # Cria novo usuário
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Gera token
        token = new_user.generate_token()
        
        return jsonify({
            'message': 'Usuário criado com sucesso!',
            'username': new_user.username,
            'email': new_user.email,
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        # Busca usuário no banco
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'message': 'Credenciais inválidas!'}), 401
        
        if not check_password(password, user.password_hash):
            return jsonify({'message': 'Credenciais inválidas!'}), 401
        
        # Atualiza último login
        user.last_login = datetime.now(timezone.utc)

        db.session.commit()
        
        # Gera token
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login realizado com sucesso!',
            'username': user.username,
            'token': token
        })
        
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

@app.route('/users', methods=['GET'])
def list_users():
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'message': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Auth Service com SQLite iniciando na porta 8001...")
    app.run(debug=True, host='0.0.0.0', port=8001)