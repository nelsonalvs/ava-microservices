from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dados de exemplo - materiais didáticos
learning_materials = [
    {
        "id": 1, 
        "title": "Python Básico", 
        "tags": ["programming", "python", "beginner"], 
        "type": "video", 
        "difficulty": "beginner",
        "description": "Introdução à programação com Python"
    },
    {
        "id": 2, 
        "title": "Algoritmos e Estruturas de Dados", 
        "tags": ["algorithms", "data-structures", "intermediate"], 
        "type": "article", 
        "difficulty": "intermediate",
        "description": "Conceitos fundamentais de algoritmos"
    },
    {
        "id": 3, 
        "title": "Desenvolvimento Web com Flask", 
        "tags": ["web", "flask", "python", "backend"], 
        "type": "course", 
        "difficulty": "intermediate",
        "description": "Crie aplicações web com Flask"
    },
    {
        "id": 4, 
        "title": "Git e Controle de Versão", 
        "tags": ["git", "github", "version-control", "beginner"], 
        "type": "tutorial", 
        "difficulty": "beginner",
        "description": "Aprenda a usar Git e GitHub"
    },
    {
        "id": 5, 
        "title": "APIs REST", 
        "tags": ["api", "rest", "web-services", "intermediate"], 
        "type": "video", 
        "difficulty": "intermediate",
        "description": "Construa APIs RESTful"
    },
    {
        "id": 6, 
        "title": "Banco de Dados SQL", 
        "tags": ["database", "sql", "queries", "intermediate"], 
        "type": "article", 
        "difficulty": "intermediate",
        "description": "Fundamentos de bancos de dados relacionais"
    }
]

# Histórico de usuários (simulado)
user_history = {}

def simple_recommend(user_interests, materials, top_n=3):
    """Recomendação simples baseada em matching de tags"""
    scored_materials = []
    
    for material in materials:
        score = 0
        # Calcula score baseado na intersecção de tags
        common_tags = set(user_interests) & set(material["tags"])
        score = len(common_tags)
        
        # Bonus por dificuldade matching (simplificado)
        if "beginner" in user_interests and material["difficulty"] == "beginner":
            score += 2
        elif "intermediate" in user_interests and material["difficulty"] == "intermediate":
            score += 2
        elif "advanced" in user_interests and material["difficulty"] == "advanced":
            score += 2
            
        scored_materials.append((material, score))
    
    # Ordena por score e retorna os top N
    scored_materials.sort(key=lambda x: x[1], reverse=True)
    return [material for material, score in scored_materials[:top_n] if score > 0]

@app.route('/')
def home():
    return jsonify({
        'message': 'Recommendation Service está rodando!',
        'total_materials': len(learning_materials),
        'version': 'simplified'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint principal de recomendação"""
    data = request.get_json()
    
    if not data or 'interests' not in data:
        return jsonify({'error': 'Interesses do usuário são obrigatórios'}), 400
    
    user_interests = data['interests']
    user_id = data.get('user_id', 'anonymous')
    top_n = data.get('top_n', 3)
    
    # Valida interesses
    if not isinstance(user_interests, list):
        return jsonify({'error': 'Interesses devem ser uma lista'}), 400
    
    # Atualiza histórico do usuário
    if user_id not in user_history:
        user_history[user_id] = []
    user_history[user_id].extend(user_interests)
    
    # Gera recomendações
    recommendations = simple_recommend(user_interests, learning_materials, top_n)
    
    # Se não encontrou recomendações, retorna materiais populares
    if not recommendations:
        recommendations = learning_materials[:top_n]
    
    return jsonify({
        'user_id': user_id,
        'user_interests': user_interests,
        'recommendations': recommendations,
        'total_recommended': len(recommendations)
    })

@app.route('/materials', methods=['GET'])
def get_materials():
    """Retorna todos os materiais disponíveis"""
    return jsonify({
        'materials': learning_materials,
        'total': len(learning_materials)
    })

@app.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Retorna um material específico"""
    material = next((m for m in learning_materials if m["id"] == material_id), None)
    if material:
        return jsonify(material)
    return jsonify({'error': 'Material não encontrado'}), 404

@app.route('/tags', methods=['GET'])
def get_tags():
    """Retorna todas as tags disponíveis"""
    all_tags = list(set(tag for material in learning_materials for tag in material["tags"]))
    return jsonify({
        'tags': all_tags,
        'total': len(all_tags)
    })

@app.route('/user/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Retorna o histórico de interesses do usuário"""
    history = user_history.get(user_id, [])
    return jsonify({
        'user_id': user_id,
        'interests_history': history
    })

if __name__ == '__main__':
    print("🚀 Iniciando Recommendation Service (Simplificado) na porta 8002...")
    app.run(debug=True, host='0.0.0.0', port=8002)