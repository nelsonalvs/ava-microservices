from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)  # Permite requests do frontend

# Configurações
app.config['SECRET_KEY'] = 'ava_secret_key_2024'

# "Banco de dados" em memória
users_db = {}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401
        
        try:
            # Remove 'Bearer ' do token
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({'message': 'Token é inválido!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def create_jwt_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/')
def home():
    return jsonify({'message': 'Auth Service está rodando!'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
    
    if username in users_db:
        return jsonify({'message': 'Usuário já existe!'}), 400
    
    users_db[username] = {
        'email': email,
        'password': password
    }
    
    token = create_jwt_token(username)
    
    return jsonify({
        'message': 'Usuário criado com sucesso!',
        'username': username,
        'email': email,
        'token': token
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if username not in users_db:
        return jsonify({'message': 'Credenciais inválidas!'}), 401
    
    if users_db[username]['password'] != password:
        return jsonify({'message': 'Credenciais inválidas!'}), 401
    
    token = create_jwt_token(username)
    
    return jsonify({
        'message': 'Login realizado com sucesso!',
        'username': username,
        'token': token
    })

@app.route('/users', methods=['GET'])
@token_required
def list_users(current_user):
    return jsonify({'users': list(users_db.keys())})

@app.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    user_data = users_db.get(current_user)
    if user_data:
        return jsonify({
            'username': current_user,
            'email': user_data['email']
        })
    return jsonify({'message': 'Usuário não encontrado!'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)