# run.py
from app.main import app

if __name__ == '__main__':
    print("🚀 Iniciando API Gateway na porta 8000...")
    app.run(debug=True, host='0.0.0.0', port=8000)