from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==================== BASE DE DADOS DE LIVROS ====================
learning_materials = [
    # === PROGRAMAÇÃO (6 livros) ===
    {
        "id": 1, "title": "Python Fluente", "author": "Luciano Ramalho", 
        "tags": ["programacao", "python", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "programacao", "nivel": 3,
        "description": "Python avançado com patterns e boas práticas",
        "image": "📘", "pages": 800, "year": 2015
    },
    {
        "id": 2, "title": "Algoritmos: Teoria e Prática", "author": "Cormen", 
        "tags": ["programacao", "algoritmos", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "programacao", "nivel": 2,
        "description": "Clássico sobre estrutura de dados e algoritmos",
        "image": "📗", "pages": 1200, "year": 2009
    },
    {
        "id": 3, "title": "Clean Code", "author": "Robert Martin", 
        "tags": ["programacao", "boas-praticas", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "programacao", "nivel": 2,
        "description": "Artesanato de software e código limpo",
        "image": "📕", "pages": 464, "year": 2008
    },
    {
        "id": 4, "title": "Introdução à Programação com Python", "author": "Nilo Ney", 
        "tags": ["programacao", "python", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "programacao", "nivel": 1,
        "description": "Fundamentos da programação usando Python",
        "image": "📓", "pages": 300, "year": 2014
    },
    {
        "id": 5, "title": "Estruturas de Dados e Algoritmos em Python", "author": "Michael T. Goodrich", 
        "tags": ["programacao", "estrutura-dados", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "programacao", "nivel": 2,
        "description": "Estruturas de dados implementadas em Python",
        "image": "📙", "pages": 700, "year": 2013
    },
    {
        "id": 6, "title": "Design Patterns: Elements of Reusable Object-Oriented Software", 
        "author": "Gang of Four", "tags": ["programacao", "design-patterns", "avancado"], 
        "type": "livro", "difficulty": "avancado", "area": "programacao", "nivel": 3,
        "description": "Padrões de projeto clássicos",
        "image": "📘", "pages": 416, "year": 1994
    },

    # === CÁLCULO (6 livros) ===
    {
        "id": 7, "title": "Cálculo Volume 1", "author": "James Stewart", 
        "tags": ["calculo", "limites", "derivadas", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "calculo", "nivel": 1,
        "description": "Limites, derivadas e aplicações",
        "image": "📐", "pages": 600, "year": 2013
    },
    {
        "id": 8, "title": "Cálculo Volume 2", "author": "James Stewart", 
        "tags": ["calculo", "integrais", "series", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "calculo", "nivel": 2,
        "description": "Integrais, séries e equações diferenciais",
        "image": "📐", "pages": 650, "year": 2013
    },
    {
        "id": 9, "title": "Cálculo com Geometria Analítica Volume 1", "author": "Louis Leithold", 
        "tags": ["calculo", "geometria-analitica", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "calculo", "nivel": 1,
        "description": "Cálculo diferencial e integral com geometria",
        "image": "📐", "pages": 800, "year": 1994
    },
    {
        "id": 10, "title": "Cálculo Avançado", "author": "Murray Spiegel", 
        "tags": ["calculo", "avancado", "variaveis-complexas"], "type": "livro", 
        "difficulty": "avancado", "area": "calculo", "nivel": 3,
        "description": "Análise complexa e cálculo avançado",
        "image": "📐", "pages": 450, "year": 1974
    },
    {
        "id": 11, "title": "Cálculo Numérico", "author": "Ruggiero & Lopes", 
        "tags": ["calculo", "numerico", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "calculo", "nivel": 2,
        "description": "Métodos numéricos para cálculo",
        "image": "📐", "pages": 500, "year": 1997
    },
    {
        "id": 12, "title": "Equações Diferenciais Elementares", "author": "William Boyce", 
        "tags": ["calculo", "equacoes-diferenciais", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "calculo", "nivel": 2,
        "description": "Equações diferenciais ordinárias e aplicações",
        "image": "📐", "pages": 600, "year": 2015
    },

    # === MATEMÁTICA DISCRETA (6 livros) ===
    {
        "id": 13, "title": "Matemática Discreta e suas Aplicações", "author": "Kenneth Rosen", 
        "tags": ["matematica-discreta", "iniciante", "logica"], "type": "livro", 
        "difficulty": "iniciante", "area": "matematica-discreta", "nivel": 1,
        "description": "Introdução à matemática discreta",
        "image": "🔢", "pages": 1000, "year": 2009
    },
    {
        "id": 14, "title": "Introdução à Teoria dos Grafos", "author": "Wilson R. Johnson", 
        "tags": ["matematica-discreta", "grafos", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "matematica-discreta", "nivel": 2,
        "description": "Teoria dos grafos e aplicações",
        "image": "🔢", "pages": 300, "year": 1995
    },
    {
        "id": 15, "title": "Lógica para Computação", "author": "Flávio Soares Corrêa", 
        "tags": ["matematica-discreta", "logica", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "matematica-discreta", "nivel": 2,
        "description": "Lógica matemática aplicada à computação",
        "image": "🔢", "pages": 350, "year": 2009
    },
    {
        "id": 16, "title": "Teoria dos Números", "author": "José Plínio de Oliveira Santos", 
        "tags": ["matematica-discreta", "teoria-numeros", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "matematica-discreta", "nivel": 3,
        "description": "Teoria dos números para computação",
        "image": "🔢", "pages": 400, "year": 2014
    },
    {
        "id": 17, "title": "Combinatória e Grafos", "author": "Cláudia Linhares Sales", 
        "tags": ["matematica-discreta", "combinatoria", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "matematica-discreta", "nivel": 2,
        "description": "Combinatória e teoria dos grafos",
        "image": "🔢", "pages": 280, "year": 2010
    },
    {
        "id": 18, "title": "Álgebra Booleana e Aplicações", "author": "Francisco de Assis Magalhães Gomes", 
        "tags": ["matematica-discreta", "algebra-booleana", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "matematica-discreta", "nivel": 3,
        "description": "Álgebra booleana e circuitos lógicos",
        "image": "🔢", "pages": 320, "year": 2005
    },

    # === FÍSICA (6 livros) ===
    {
        "id": 19, "title": "Física Universitária Volume 1", "author": "Young & Freedman", 
        "tags": ["fisica", "mecanica", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "fisica", "nivel": 1,
        "description": "Mecânica, oscilações e ondas",
        "image": "⚛️", "pages": 700, "year": 2016
    },
    {
        "id": 20, "title": "Física para Cientistas e Engenheiros", "author": "Paul Tipler", 
        "tags": ["fisica", "eletromagnetismo", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "fisica", "nivel": 2,
        "description": "Eletromagnetismo e física moderna",
        "image": "⚛️", "pages": 900, "year": 2009
    },
    {
        "id": 21, "title": "Fundamentos de Física Volume 1", "author": "Halliday & Resnick", 
        "tags": ["fisica", "mecanica", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "fisica", "nivel": 1,
        "description": "Mecânica clássica e termodinâmica",
        "image": "⚛️", "pages": 350, "year": 2018
    },
    {
        "id": 22, "title": "Física Quântica", "author": "Eisberg & Resnick", 
        "tags": ["fisica", "quantica", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "fisica", "nivel": 3,
        "description": "Introdução à física quântica",
        "image": "⚛️", "pages": 500, "year": 1994
    },
    {
        "id": 23, "title": "Termodinâmica", "author": "Çengel & Boles", 
        "tags": ["fisica", "termodinamica", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "fisica", "nivel": 2,
        "description": "Termodinâmica para engenharia",
        "image": "⚛️", "pages": 600, "year": 2013
    },
    {
        "id": 24, "title": "Óptica", "author": "Eugene Hecht", 
        "tags": ["fisica", "optica", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "fisica", "nivel": 2,
        "description": "Fundamentos da óptica física e geométrica",
        "image": "⚛️", "pages": 700, "year": 2016
    },

    # === ENGENHARIA DE SOFTWARE (6 livros) ===
    {
        "id": 25, "title": "Engenharia de Software", "author": "Ian Sommerville", 
        "tags": ["engenharia-software", "processos", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "engenharia-software", "nivel": 2,
        "description": "Processos de engenharia de software",
        "image": "💻", "pages": 800, "year": 2011
    },
    {
        "id": 26, "title": "UML: Guia do Usuário", "author": "Grady Booch", 
        "tags": ["engenharia-software", "uml", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "engenharia-software", "nivel": 1,
        "description": "Modelagem de software com UML",
        "image": "💻", "pages": 500, "year": 2012
    },
    {
        "id": 27, "title": "Padrões de Projeto", "author": "Erich Gamma", 
        "tags": ["engenharia-software", "design-patterns", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "engenharia-software", "nivel": 3,
        "description": "Padrões de projeto orientados a objetos",
        "image": "💻", "pages": 400, "year": 1994
    },
    {
        "id": 28, "title": "Arquitetura Limpa", "author": "Robert Martin", 
        "tags": ["engenharia-software", "arquitetura", "avancado"], "type": "livro", 
        "difficulty": "avancado", "area": "engenharia-software", "nivel": 3,
        "description": "Arquitetura e design de software",
        "image": "💻", "pages": 350, "year": 2017
    },
    {
        "id": 29, "title": "Scrum: Guia Prático", "author": "Ken Schwaber", 
        "tags": ["engenharia-software", "scrum", "iniciante"], "type": "livro", 
        "difficulty": "iniciante", "area": "engenharia-software", "nivel": 1,
        "description": "Metodologias ágeis e Scrum",
        "image": "💻", "pages": 200, "year": 2004
    },
    {
        "id": 30, "title": "Test-Driven Development", "author": "Kent Beck", 
        "tags": ["engenharia-software", "tdd", "intermediario"], "type": "livro", 
        "difficulty": "intermediario", "area": "engenharia-software", "nivel": 2,
        "description": "Desenvolvimento guiado por testes",
        "image": "💻", "pages": 240, "year": 2002
    }
]

# Definição das áreas disponíveis
AREAS = {
    "programacao": "Programação",
    "calculo": "Cálculo", 
    "matematica-discreta": "Matemática Discreta",
    "fisica": "Física",
    "engenharia-software": "Engenharia de Software"
}

NIVEIS = {
    1: "iniciante",
    2: "intermediario", 
    3: "avancado"
}

# Histórico de usuários
user_history = {}

def advanced_recommend(user_areas, user_nivel, materials, top_n=6):
    """Sistema de recomendação por áreas selecionadas e nível"""
    scored_materials = []
    
    for material in materials:
        score = 0
        
        # 1. Score por área selecionada (MAIS IMPORTANTE)
        if material["area"] in user_areas:
            score += 10  # Peso máximo para área selecionada
            
            # 2. Score por nível (dentro da área selecionada)
            nivel_diff = abs(user_nivel - material["nivel"])
            if nivel_diff == 0:
                score += 5  # Nível perfeito
            elif nivel_diff == 1:
                score += 3  # Nível próximo
            elif nivel_diff == 2:
                score += 1  # Nível distante
        
        # 3. Bônus para materiais do mesmo nível (mesmo que não seja da área)
        if material["nivel"] == user_nivel:
            score += 2
            
        scored_materials.append((material, score))
    
    # Filtra apenas materiais com score > 0 (pelo menos da área certa)
    scored_materials = [(material, score) for material, score in scored_materials if score > 0]
    
    # Ordena por score
    scored_materials.sort(key=lambda x: x[1], reverse=True)
    
    # Retorna os top N
    return [material for material, score in scored_materials[:top_n]]

@app.route('/')
def home():
    return jsonify({
        'message': 'Sistema de Recomendações Avançado - 5 Áreas, 30 Livros',
        'total_materials': len(learning_materials),
        'areas': AREAS,
        'niveis': NIVEIS
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint principal de recomendação por áreas"""
    data = request.get_json()
    
    if not data or 'areas' not in data:
        return jsonify({'error': 'Áreas de interesse são obrigatórias'}), 400
    
    user_areas = data['areas']  # Lista de áreas selecionadas
    user_id = data.get('user_id', 'anonymous')
    user_nivel = data.get('nivel', 1)  # Nível padrão: 1 (iniciante)
    top_n = data.get('top_n', 6)
    
    # Valida áreas
    if not isinstance(user_areas, list):
        return jsonify({'error': 'Áreas devem ser uma lista'}), 400
    
    # Valida se as áreas existem
    for area in user_areas:
        if area not in AREAS:
            return jsonify({'error': f'Área "{area}" não existe'}), 400
    
    # Atualiza histórico do usuário
    if user_id not in user_history:
        user_history[user_id] = {"areas": [], "nivel": user_nivel}
    user_history[user_id]["areas"].extend(user_areas)
    
    # Gera recomendações avançadas
    recommendations = advanced_recommend(user_areas, user_nivel, learning_materials, top_n)
    
    return jsonify({
        'user_id': user_id,
        'user_nivel': user_nivel,
        'user_areas': user_areas,
        'recommendations': recommendations,
        'total_recommended': len(recommendations),
        'algorithm': 'advanced-areas'
    })

@app.route('/materials', methods=['GET'])
def get_materials():
    """Retorna todos os materiais disponíveis"""
    return jsonify({
        'materials': learning_materials,
        'total': len(learning_materials),
        'areas': {area: len([m for m in learning_materials if m['area'] == area]) 
                 for area in AREAS}
    })

@app.route('/materials/area/<area_name>', methods=['GET'])
def get_materials_by_area(area_name):
    """Retorna materiais por área específica"""
    if area_name not in AREAS:
        return jsonify({'error': 'Área não encontrada'}), 404
        
    area_materials = [m for m in learning_materials if m['area'] == area_name]
    return jsonify({
        'area': area_name,
        'area_name': AREAS[area_name],
        'materials': area_materials,
        'total': len(area_materials)
    })

@app.route('/areas', methods=['GET'])
def get_areas():
    """Retorna todas as áreas disponíveis"""
    return jsonify({
        'areas': AREAS,
        'total': len(AREAS)
    })

@app.route('/niveis', methods=['GET'])
def get_niveis():
    """Retorna todos os níveis disponíveis"""
    return jsonify({
        'niveis': NIVEIS,
        'total': len(NIVEIS)
    })

@app.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    """Retorna um material específico"""
    material = next((m for m in learning_materials if m["id"] == material_id), None)
    if material:
        return jsonify(material)
    return jsonify({'error': 'Material não encontrado'}), 404

@app.route('/user/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Retorna o histórico do usuário"""
    history = user_history.get(user_id, {"areas": [], "nivel": 1})
    return jsonify({
        'user_id': user_id,
        'areas_history': history["areas"],
        'current_nivel': history.get("nivel", 1)
    })

@app.route('/user/<user_id>/nivel', methods=['POST'])
def update_user_nivel(user_id):
    """Atualiza o nível do usuário"""
    data = request.get_json()
    new_nivel = data.get('nivel', 1)
    
    if new_nivel not in [1, 2, 3]:
        return jsonify({'error': 'Nível deve ser 1, 2 ou 3'}), 400
    
    if user_id not in user_history:
        user_history[user_id] = {"areas": [], "nivel": new_nivel}
    else:
        user_history[user_id]["nivel"] = new_nivel
    
    return jsonify({
        'user_id': user_id,
        'new_nivel': new_nivel,
        'nivel_texto': NIVEIS[new_nivel],
        'message': 'Nível atualizado com sucesso'
    })

if __name__ == '__main__':
    print("🚀 Sistema de Recomendações Avançado - 5 Áreas, 30 Livros")
    print("📚 Áreas disponíveis:", list(AREAS.keys()))
    print("🎯 Níveis: Iniciante (1), Intermediário (2), Avançado (3)")
    app.run(debug=True, host='0.0.0.0', port=8002)