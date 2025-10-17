# ava-microservices

# 🎓 AVA - Ambiente Virtual de Aprendizagem

Sistema de ensino online com microserviços e sistema de recomendações inteligente.

## 🚀 Funcionalidades

### 🔐 Autenticação
- Registro e login de usuários
- Autenticação JWT
- Banco de dados SQLite

### 📚 Sistema de Recomendações
- **5 Áreas de Conhecimento:**
  - 💻 Programação
  - 📐 Cálculo
  - 🔢 Matemática Discreta
  - ⚛️ Física
  - 🏗️ Engenharia de Software

- **3 Níveis de Dificuldade:**
  - 🥚 Iniciante (1)
  - 🐣 Intermediário (2)
  - 🦅 Avançado (3)

- **30 Livros** com informações completas

### 📖 Lista Pessoal
- Adicionar livros à lista pessoal
- Status: Quero Ler, Lendo, Lido
- Remover livros da lista

## 🛠️ Tecnologias

- **Backend:** Python, Flask, SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Banco:** SQLite
- **Autenticação:** JWT

## 📋 Como Rodar

### Pré-requisitos
- Python 3.8+
- Git
- Navegador web

### 🚀 Comandos para Executar

**Abra 4 terminais separados:**

#### Terminal 1 - Auth Service:
```bash
- cd C:\ava-microservices\backend\microservices\auth-service
- python run.py

- NOVO TERMINAL:

- cd C:\ava-microservices\backend\microservices\recommendation-service
- python run.py

- NOVO TERMINAL:

- cd C:\ava-microservices\backend\api-gateway
- python run.py

- NOVO TERMINAL:

- cd C:\ava-microservices\frontend
- start index.html



## 🌐 Acesso

- **Sistema:** `frontend/index.html`
- **API:** `http://localhost:8000`

## 🎯 Como Usar

1. **Acesse** `frontend/index.html`
2. **Cadastre-se** ou faça login
3. **Selecione** áreas e nível
4. **Gere recomendações**
5. **Adicione livros** à lista
6. **Acompanhe** progresso


## 🏗️ Estrutura do Projeto

ava-microservices/
├── frontend/
│ ├── index.html
│ ├── login.html
│ ├── dashboard.html
│ ├── css/
│ │ └── style.css
│ └── js/
│ ├── auth.js
│ └── recommendations.js
├── backend/
│ ├── api-gateway/
│ │ ├── app/
│ │ │ └── main.py
│ │ └── requirements.txt
│ └── microservices/
│ ├── auth-service/
│ │ ├── app/
│ │ │ ├── main.py
│ │ │ ├── models.py
│ │ │ └── database.py
│ │ └── requirements.txt
│ └── recommendation-service/
│ ├── app/
│ │ ├── main.py
│ │ ├── models.py
│ │ └── database.py
│ └── requirements.txt
└── README.md

## 🔗 Endpoints da API

### Auth Service

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/auth/register` | Registrar novo usuário |
| `POST` | `/auth/login` | Fazer login |
| `GET` | `/auth/health` | Status do serviço |
| `GET` | `/auth/users` | Listar usuários |

#### Exemplo de Request - Register:
```json
{
  "username": "usuario",
  "email": "usuario@email.com",
  "password": "senha123"
}

## 🔗 Endpoints da API

### Recommendation Service

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/recommendation/recommend` | Gerar recomendações personalizadas |
| `GET` | `/recommendation/materials` | Listar todos os 30 materiais |
| `GET` | `/recommendation/materials/area/{area_name}` | Filtrar materiais por área |
| `GET` | `/recommendation/areas` | Listar áreas disponíveis |
| `GET` | `/recommendation/niveis` | Listar níveis disponíveis |
| `GET` | `/recommendation/materials/{material_id}` | Buscar material específico |
| `POST` | `/recommendation/user/{user_id}/booklist` | Adicionar livro à lista pessoal |
| `GET` | `/recommendation/user/{user_id}/booklist` | Visualizar lista pessoal |
| `DELETE` | `/recommendation/user/{user_id}/booklist/{book_id}` | Remover livro da lista |
| `PUT` | `/recommendation/user/{user_id}/booklist/{book_id}/status` | Atualizar status do livro |
| `POST` | `/recommendation/user/{user_id}/level` | Atualizar nível do usuário |
| `GET` | `/recommendation/user/{user_id}/history` | Ver histórico do usuário |

#### Exemplo de Request - Recomendação:
```json
{
  "user_id": "usuario123",
  "areas": ["programacao", "calculo"],
  "nivel": 2,
  "top_n": 6
}


## 💾 Implementação do Banco de Dados

### Arquitetura do Banco

O sistema utiliza **SQLite** como banco de dados relacional, com arquivos separados para cada microserviço:

- `auth_service.db` - Banco do Auth Service (Porta 8001)
- `recommendation_service.db` - Banco do Recommendation Service (Porta 8002)

### Estrutura das Tabelas

#### Tabela: users (Auth Service)
| Coluna | Tipo | Descrição | Restrições |
|--------|------|-----------|------------|
| `id` | INTEGER | ID único do usuário | PRIMARY KEY, AUTOINCREMENT |
| `username` | VARCHAR(80) | Nome de usuário | UNIQUE, NOT NULL |
| `email` | VARCHAR(120) | Email do usuário | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(200) | Hash da senha (bcrypt) | NOT NULL |
| `created_at` | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |
| `last_login` | DATETIME | Último acesso | NULLABLE |

#### Tabela: learning_materials (Recommendation Service)
| Coluna | Tipo | Descrição | Restrições |
|--------|------|-----------|------------|
| `id` | INTEGER | ID único do material | PRIMARY KEY, AUTOINCREMENT |
| `title` | VARCHAR(200) | Título do livro | NOT NULL |
| `author` | VARCHAR(100) | Autor do livro | NOT NULL |
| `tags` | VARCHAR(500) | Tags categorizadas | Formato: "tag1,tag2,tag3" |
| `type` | VARCHAR(50) | Tipo de material | NOT NULL |
| `difficulty` | VARCHAR(50) | Nível de dificuldade | NOT NULL |
| `area` | VARCHAR(50) | Área de conhecimento | NOT NULL |
| `nivel` | INTEGER | Nível numérico (1-3) | NOT NULL |
| `description` | TEXT | Descrição detalhada | NULLABLE |
| `image` | VARCHAR(10) | Emoji representativo | NULLABLE |
| `pages` | INTEGER | Número de páginas | NULLABLE |
| `year` | INTEGER | Ano de publicação | NULLABLE |
| `created_at` | DATETIME | Data de inserção | DEFAULT CURRENT_TIMESTAMP |

#### Tabela: user_book_lists (Recommendation Service)
| Coluna | Tipo | Descrição | Restrições |
|--------|------|-----------|------------|
| `id` | INTEGER | ID único do registro | PRIMARY KEY, AUTOINCREMENT |
| `user_id` | VARCHAR(100) | Identificador do usuário | NOT NULL |
| `material_id` | INTEGER | Referência ao material | FOREIGN KEY |
| `added_at` | DATETIME | Data de adição | DEFAULT CURRENT_TIMESTAMP |
| `status` | VARCHAR(50) | Status de leitura | DEFAULT 'quero_ler' |

#### Tabela: user_history (Recommendation Service)
| Coluna | Tipo | Descrição | Restrições |
|--------|------|-----------|------------|
| `id` | INTEGER | ID único do histórico | PRIMARY KEY, AUTOINCREMENT |
| `user_id` | VARCHAR(100) | Identificador do usuário | NOT NULL |
| `areas` | VARCHAR(500) | Áreas de interesse | Formato: "area1,area2" |
| `nivel` | INTEGER | Nível atual do usuário | DEFAULT 1 |
| `created_at` | DATETIME | Data de criação | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | DATETIME | Última atualização | DEFAULT CURRENT_TIMESTAMP |

### Funcionamento do Banco

#### Inicialização Automática
```python
# Ao iniciar o Recommendation Service, o banco é populado automaticamente
def populate_database():
    if LearningMaterial.query.count() == 0:
        # Insere os 30 materiais iniciais
        materials = [
            LearningMaterial(title="Python Fluente", ...),
            LearningMaterial(title="Cálculo Volume 1", ...),
            # ... 28 materiais restantes
        ]
        db.session.bulk_save_objects(materials)
        db.session.commit()


## 💾 Banco de Dados

### Como Funciona

O sistema usa dois bancos de dados SQLite separados: um para autenticação e outro para recomendações.

### Estrutura dos Bancos

**Auth Service (auth_service.db)**
- Tabela `users`: armazena informações dos usuários (nome, email, senha criptografada)

**Recommendation Service (recommendation_service.db)**
- Tabela `learning_materials`: 30 livros com informações completas
- Tabela `user_book_lists`: lista pessoal de livros de cada usuário
- Tabela `user_history`: histórico de interesses do usuário

### Fluxo de Dados

1. Usuário se cadastra → dados salvos na tabela `users`
2. Usuário faz login → sistema verifica credenciais
3. Usuário seleciona áreas de interesse → salvo em `user_history`
4. Sistema gera recomendações → baseado nas áreas e nível do usuário
5. Usuário adiciona livros à lista → salvos em `user_book_lists`

### Sistema de Recomendações

O sistema recomenda livros considerando:
- Áreas de interesse selecionadas pelo usuário
- Nível de conhecimento do usuário (iniciante, intermediário, avançado)
- Compatibilidade entre tags dos livros e interesses do usuário

### Segurança

- Senhas são criptografadas usando bcrypt
- Cada microserviço tem seu banco independente
- Prevenção contra SQL injection via SQLAlchemy ORM

### Vantagens

- Fácil configuração (SQLite não requer instalação)
- Dados persistentes entre sessões
- Separado por microserviços
- Ideal para desenvolvimento e testes

### Manutenção

Para reiniciar o banco de dados:
- Delete os arquivos `.db`
- Reinicie os serviços
- Os bancos são recriados automaticamente com dados iniciais