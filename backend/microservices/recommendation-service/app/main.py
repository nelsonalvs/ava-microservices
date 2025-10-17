from flask import Flask, request, jsonify
from flask_cors import CORS
from .database import db, init_db
from .models import LearningMaterial, UserHistory, UserBookList
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# Inicializa o banco de dados
init_db(app)

# ==================== CONFIGURAÇÃO ====================
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

# ==================== POPULAR BANCO ====================
def populate_database():
    """Popula o banco com todos os 30 livros se estiver vazio"""
    if LearningMaterial.query.count() == 0:
        materials = [
            # === PROGRAMAÇÃO (6 livros) ===
            LearningMaterial(
                title="Python Fluente", author="Luciano Ramalho",
                tags="programacao,python,avancado", type="livro",
                difficulty="avancado", area="programacao", nivel=3,
                description="Python avançado com patterns e boas práticas",
                image="📘", pages=800, year=2015
            ),
            LearningMaterial(
                title="Algoritmos: Teoria e Prática", author="Cormen",
                tags="programacao,algoritmos,intermediario", type="livro",
                difficulty="intermediario", area="programacao", nivel=2,
                description="Clássico sobre estrutura de dados e algoritmos",
                image="📗", pages=1200, year=2009
            ),
            LearningMaterial(
                title="Clean Code", author="Robert Martin",
                tags="programacao,boas-praticas,intermediario", type="livro",
                difficulty="intermediario", area="programacao", nivel=2,
                description="Artesanato de software e código limpo",
                image="📕", pages=464, year=2008
            ),
            LearningMaterial(
                title="Introdução à Programação com Python", author="Nilo Ney",
                tags="programacao,python,iniciante", type="livro",
                difficulty="iniciante", area="programacao", nivel=1,
                description="Fundamentos da programação usando Python",
                image="📓", pages=300, year=2014
            ),
            LearningMaterial(
                title="Estruturas de Dados e Algoritmos em Python", author="Michael T. Goodrich",
                tags="programacao,estrutura-dados,intermediario", type="livro",
                difficulty="intermediario", area="programacao", nivel=2,
                description="Estruturas de dados implementadas em Python",
                image="📙", pages=700, year=2013
            ),
            LearningMaterial(
                title="Design Patterns: Elements of Reusable Object-Oriented Software", 
                author="Gang of Four", tags="programacao,design-patterns,avancado", 
                type="livro", difficulty="avancado", area="programacao", nivel=3,
                description="Padrões de projeto clássicos",
                image="📘", pages=416, year=1994
            ),

            # === CÁLCULO (6 livros) ===
            LearningMaterial(
                title="Cálculo Volume 1", author="James Stewart",
                tags="calculo,limites,derivadas,iniciante", type="livro",
                difficulty="iniciante", area="calculo", nivel=1,
                description="Limites, derivadas e aplicações",
                image="📐", pages=600, year=2013
            ),
            LearningMaterial(
                title="Cálculo Volume 2", author="James Stewart",
                tags="calculo,integrais,series,intermediario", type="livro",
                difficulty="intermediario", area="calculo", nivel=2,
                description="Integrais, séries e equações diferenciais",
                image="📐", pages=650, year=2013
            ),
            LearningMaterial(
                title="Cálculo com Geometria Analítica Volume 1", author="Louis Leithold",
                tags="calculo,geometria-analitica,iniciante", type="livro",
                difficulty="iniciante", area="calculo", nivel=1,
                description="Cálculo diferencial e integral com geometria",
                image="📐", pages=800, year=1994
            ),
            LearningMaterial(
                title="Cálculo Avançado", author="Murray Spiegel",
                tags="calculo,avancado,variaveis-complexas", type="livro",
                difficulty="avancado", area="calculo", nivel=3,
                description="Análise complexa e cálculo avançado",
                image="📐", pages=450, year=1974
            ),
            LearningMaterial(
                title="Cálculo Numérico", author="Ruggiero & Lopes",
                tags="calculo,numerico,intermediario", type="livro",
                difficulty="intermediario", area="calculo", nivel=2,
                description="Métodos numéricos para cálculo",
                image="📐", pages=500, year=1997
            ),
            LearningMaterial(
                title="Equações Diferenciais Elementares", author="William Boyce",
                tags="calculo,equacoes-diferenciais,intermediario", type="livro",
                difficulty="intermediario", area="calculo", nivel=2,
                description="Equações diferenciais ordinárias e aplicações",
                image="📐", pages=600, year=2015
            ),

            # === MATEMÁTICA DISCRETA (6 livros) ===
            LearningMaterial(
                title="Matemática Discreta e suas Aplicações", author="Kenneth Rosen",
                tags="matematica-discreta,iniciante,logica", type="livro",
                difficulty="iniciante", area="matematica-discreta", nivel=1,
                description="Introdução à matemática discreta",
                image="🔢", pages=1000, year=2009
            ),
            LearningMaterial(
                title="Introdução à Teoria dos Grafos", author="Wilson R. Johnson",
                tags="matematica-discreta,grafos,intermediario", type="livro",
                difficulty="intermediario", area="matematica-discreta", nivel=2,
                description="Teoria dos grafos e aplicações",
                image="🔢", pages=300, year=1995
            ),
            LearningMaterial(
                title="Lógica para Computação", author="Flávio Soares Corrêa",
                tags="matematica-discreta,logica,intermediario", type="livro",
                difficulty="intermediario", area="matematica-discreta", nivel=2,
                description="Lógica matemática aplicada à computação",
                image="🔢", pages=350, year=2009
            ),
            LearningMaterial(
                title="Teoria dos Números", author="José Plínio de Oliveira Santos",
                tags="matematica-discreta,teoria-numeros,avancado", type="livro",
                difficulty="avancado", area="matematica-discreta", nivel=3,
                description="Teoria dos números para computação",
                image="🔢", pages=400, year=2014
            ),
            LearningMaterial(
                title="Combinatória e Grafos", author="Cláudia Linhares Sales",
                tags="matematica-discreta,combinatoria,intermediario", type="livro",
                difficulty="intermediario", area="matematica-discreta", nivel=2,
                description="Combinatória e teoria dos grafos",
                image="🔢", pages=280, year=2010
            ),
            LearningMaterial(
                title="Álgebra Booleana e Aplicações", author="Francisco de Assis Magalhães Gomes",
                tags="matematica-discreta,algebra-booleana,avancado", type="livro",
                difficulty="avancado", area="matematica-discreta", nivel=3,
                description="Álgebra booleana e circuitos lógicos",
                image="🔢", pages=320, year=2005
            ),

            # === FÍSICA (6 livros) ===
            LearningMaterial(
                title="Física Universitária Volume 1", author="Young & Freedman",
                tags="fisica,mecanica,iniciante", type="livro",
                difficulty="iniciante", area="fisica", nivel=1,
                description="Mecânica, oscilações e ondas",
                image="⚛️", pages=700, year=2016
            ),
            LearningMaterial(
                title="Física para Cientistas e Engenheiros", author="Paul Tipler",
                tags="fisica,eletromagnetismo,intermediario", type="livro",
                difficulty="intermediario", area="fisica", nivel=2,
                description="Eletromagnetismo e física moderna",
                image="⚛️", pages=900, year=2009
            ),
            LearningMaterial(
                title="Fundamentos de Física Volume 1", author="Halliday & Resnick",
                tags="fisica,mecanica,iniciante", type="livro",
                difficulty="iniciante", area="fisica", nivel=1,
                description="Mecânica clássica e termodinâmica",
                image="⚛️", pages=350, year=2018
            ),
            LearningMaterial(
                title="Física Quântica", author="Eisberg & Resnick",
                tags="fisica,quantica,avancado", type="livro",
                difficulty="avancado", area="fisica", nivel=3,
                description="Introdução à física quântica",
                image="⚛️", pages=500, year=1994
            ),
            LearningMaterial(
                title="Termodinâmica", author="Çengel & Boles",
                tags="fisica,termodinamica,intermediario", type="livro",
                difficulty="intermediario", area="fisica", nivel=2,
                description="Termodinâmica para engenharia",
                image="⚛️", pages=600, year=2013
            ),
            LearningMaterial(
                title="Óptica", author="Eugene Hecht",
                tags="fisica,optica,intermediario", type="livro",
                difficulty="intermediario", area="fisica", nivel=2,
                description="Fundamentos da óptica física e geométrica",
                image="⚛️", pages=700, year=2016
            ),

            # === ENGENHARIA DE SOFTWARE (6 livros) ===
            LearningMaterial(
                title="Engenharia de Software", author="Ian Sommerville",
                tags="engenharia-software,processos,intermediario", type="livro",
                difficulty="intermediario", area="engenharia-software", nivel=2,
                description="Processos de engenharia de software",
                image="💻", pages=800, year=2011
            ),
            LearningMaterial(
                title="UML: Guia do Usuário", author="Grady Booch",
                tags="engenharia-software,uml,iniciante", type="livro",
                difficulty="iniciante", area="engenharia-software", nivel=1,
                description="Modelagem de software com UML",
                image="💻", pages=500, year=2012
            ),
            LearningMaterial(
                title="Padrões de Projeto", author="Erich Gamma",
                tags="engenharia-software,design-patterns,avancado", type="livro",
                difficulty="avancado", area="engenharia-software", nivel=3,
                description="Padrões de projeto orientados a objetos",
                image="💻", pages=400, year=1994
            ),
            LearningMaterial(
                title="Arquitetura Limpa", author="Robert Martin",
                tags="engenharia-software,arquitetura,avancado", type="livro",
                difficulty="avancado", area="engenharia-software", nivel=3,
                description="Arquitetura e design de software",
                image="💻", pages=350, year=2017
            ),
            LearningMaterial(
                title="Scrum: Guia Prático", author="Ken Schwaber",
                tags="engenharia-software,scrum,iniciante", type="livro",
                difficulty="iniciante", area="engenharia-software", nivel=1,
                description="Metodologias ágeis e Scrum",
                image="💻", pages=200, year=2004
            ),
            LearningMaterial(
                title="Test-Driven Development", author="Kent Beck",
                tags="engenharia-software,tdd,intermediario", type="livro",
                difficulty="intermediario", area="engenharia-software", nivel=2,
                description="Desenvolvimento guiado por testes",
                image="💻", pages=240, year=2002
            )
        ]
        
        for material in materials:
            db.session.add(material)
        
        db.session.commit()
        print("✅ Banco de dados populado com 30 materiais")

# ==================== FUNÇÕES DE RECOMENDAÇÃO ====================
def advanced_recommend(user_areas, user_nivel, materials, top_n=6):
    """Sistema de recomendação por áreas selecionadas e nível"""
    scored_materials = []
    
    for material in materials:
        score = 0
        
        # 1. Score por área selecionada (MAIS IMPORTANTE)
        if material.area in user_areas:
            score += 10
            
            # 2. Score por nível
            nivel_diff = abs(user_nivel - material.nivel)
            if nivel_diff == 0:
                score += 5
            elif nivel_diff == 1:
                score += 3
            elif nivel_diff == 2:
                score += 1
        
        # 3. Bônus para mesmo nível
        if material.nivel == user_nivel:
            score += 2
            
        scored_materials.append((material, score))
    
    # Filtra e ordena
    scored_materials = [(material, score) for material, score in scored_materials if score > 0]
    scored_materials.sort(key=lambda x: x[1], reverse=True)
    
    return [material for material, score in scored_materials[:top_n]]

# ==================== ROTAS ====================
@app.route('/')
def home():
    return jsonify({
        'message': 'Sistema de Recomendações com SQLite - 5 Áreas, 30 Livros',
        'total_materials': LearningMaterial.query.count(),
        'areas': AREAS,
        'niveis': NIVEIS
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'database': 'SQLite'})

@app.route('/recommend', methods=['POST'])
def recommend():
    """Endpoint principal de recomendação"""
    data = request.get_json()
    
    if not data or 'areas' not in data:
        return jsonify({'error': 'Áreas de interesse são obrigatórias'}), 400
    
    user_areas = data['areas']
    user_id = data.get('user_id', 'anonymous')
    user_nivel = data.get('nivel', 1)
    top_n = data.get('top_n', 6)
    
    # Valida áreas
    if not isinstance(user_areas, list):
        return jsonify({'error': 'Áreas devem ser uma lista'}), 400
    
    for area in user_areas:
        if area not in AREAS:
            return jsonify({'error': f'Área "{area}" não existe'}), 400
    
    # Busca ou cria histórico do usuário
    user_history = UserHistory.query.filter_by(user_id=user_id).first()
    if user_history:
        user_history.areas = ','.join(user_areas)
        user_history.nivel = user_nivel
        user_history.updated_at = datetime.now(timezone.utc)
    else:
        user_history = UserHistory(
            user_id=user_id,
            areas=','.join(user_areas),
            nivel=user_nivel
        )
        db.session.add(user_history)
    
    db.session.commit()
    
    # Busca materiais do banco
    all_materials = LearningMaterial.query.all()
    
    # Gera recomendações
    recommendations = advanced_recommend(user_areas, user_nivel, all_materials, top_n)
    
    return jsonify({
        'user_id': user_id,
        'user_nivel': user_nivel,
        'user_areas': user_areas,
        'recommendations': [material.to_dict() for material in recommendations],
        'total_recommended': len(recommendations),
        'algorithm': 'advanced-areas-sqlite'
    })

@app.route('/materials', methods=['GET'])
def get_materials():
    """Retorna todos os materiais disponíveis"""
    materials = LearningMaterial.query.all()
    return jsonify({
        'materials': [material.to_dict() for material in materials],
        'total': len(materials),
        'areas': {area: len([m for m in materials if m.area == area]) for area in AREAS}
    })

@app.route('/materials/area/<area_name>', methods=['GET'])
def get_materials_by_area(area_name):
    """Retorna materiais por área específica"""
    if area_name not in AREAS:
        return jsonify({'error': 'Área não encontrada'}), 404
        
    materials = LearningMaterial.query.filter_by(area=area_name).all()
    return jsonify({
        'area': area_name,
        'area_name': AREAS[area_name],
        'materials': [material.to_dict() for material in materials],
        'total': len(materials)
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
    material = LearningMaterial.query.get(material_id)
    if material:
        return jsonify(material.to_dict())
    return jsonify({'error': 'Material não encontrado'}), 404

@app.route('/user/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Retorna o histórico do usuário"""
    history = UserHistory.query.filter_by(user_id=user_id).first()
    if history:
        return jsonify({
            'user_id': user_id,
            'areas_history': history.areas.split(',') if history.areas else [],
            'current_nivel': history.nivel
        })
    return jsonify({
        'user_id': user_id,
        'areas_history': [],
        'current_nivel': 1
    })

@app.route('/user/<user_id>/level', methods=['POST'])
def update_user_level(user_id):
    """Atualiza o nível do usuário"""
    data = request.get_json()
    new_nivel = data.get('level', 1)
    
    if new_nivel not in [1, 2, 3]:
        return jsonify({'error': 'Nível deve ser 1, 2 ou 3'}), 400
    
    user_history = UserHistory.query.filter_by(user_id=user_id).first()
    if user_history:
        user_history.nivel = new_nivel
        user_history.updated_at = datetime.now(timezone.utc)
    else:
        user_history = UserHistory(user_id=user_id, nivel=new_nivel)
        db.session.add(user_history)
    
    db.session.commit()
    
    return jsonify({
        'user_id': user_id,
        'new_level': new_nivel,
        'nivel_texto': NIVEIS[new_nivel],
        'message': 'Nível atualizado com sucesso'
    })

# Popula o banco na inicialização
with app.app_context():
    populate_database()

if __name__ == '__main__':
    print("🚀 Recommendation Service com SQLite - 5 Áreas, 30 Livros")
    print("📚 Áreas disponíveis:", list(AREAS.keys()))
    print("🎯 Níveis: Iniciante (1), Intermediário (2), Avançado (3)")
    app.run(debug=True, host='0.0.0.0', port=8002)


# ==================== ROTAS DA LISTA PESSOAL ====================

@app.route('/user/<user_id>/booklist', methods=['GET'])
def get_user_booklist(user_id):
    """Retorna a lista pessoal de livros do usuário"""
    try:
        user_books = UserBookList.query.filter_by(user_id=user_id).all()
        return jsonify({
            'user_id': user_id,
            'books': [book.to_dict() for book in user_books],
            'total': len(user_books)
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar lista: {str(e)}'}), 500

@app.route('/user/<user_id>/booklist', methods=['POST'])
def add_to_booklist(user_id):
    """Adiciona um livro à lista pessoal do usuário"""
    try:
        data = request.get_json()
        material_id = data.get('material_id')
        
        if not material_id:
            return jsonify({'error': 'material_id é obrigatório'}), 400
        
        # Verifica se o material existe
        material = LearningMaterial.query.get(material_id)
        if not material:
            return jsonify({'error': 'Material não encontrado'}), 404
        
        # Verifica se já está na lista
        existing = UserBookList.query.filter_by(
            user_id=user_id, 
            material_id=material_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Livro já está na sua lista'}), 400
        
        # Adiciona à lista
        new_book = UserBookList(
            user_id=user_id,
            material_id=material_id,
            status=data.get('status', 'quero_ler')
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            'message': 'Livro adicionado à sua lista!',
            'book': new_book.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao adicionar livro: {str(e)}'}), 500

@app.route('/user/<user_id>/booklist/<int:book_id>', methods=['DELETE'])
def remove_from_booklist(user_id, book_id):
    """Remove um livro da lista pessoal"""
    try:
        book = UserBookList.query.filter_by(id=book_id, user_id=user_id).first()
        
        if not book:
            return jsonify({'error': 'Livro não encontrado na sua lista'}), 404
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({'message': 'Livro removido da sua lista'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao remover livro: {str(e)}'}), 500

@app.route('/user/<user_id>/booklist/<int:book_id>/status', methods=['PUT'])
def update_book_status(user_id, book_id):
    """Atualiza o status de um livro na lista"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['quero_ler', 'lendo', 'lido']:
            return jsonify({'error': 'Status inválido'}), 400
        
        book = UserBookList.query.filter_by(id=book_id, user_id=user_id).first()
        
        if not book:
            return jsonify({'error': 'Livro não encontrado na sua lista'}), 404
        
        book.status = new_status
        db.session.commit()
        
        return jsonify({
            'message': f'Status atualizado para: {new_status}',
            'book': book.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar status: {str(e)}'}), 500