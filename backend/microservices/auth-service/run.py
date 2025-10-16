# run.py - Este arquivo fora FORA da pasta app
from app.main import app

if __name__ == '__main__':
    print("🚀 Iniciando Auth Service na porta 8001...")
    app.run(debug=True, host='0.0.0.0', port=8001)