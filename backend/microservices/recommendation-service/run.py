# run.py
from app.main import app

if __name__ == '__main__':
    print("🚀 Iniciando Recommendation Service na porta 8002...")
    app.run(debug=True, host='0.0.0.0', port=8002)


    