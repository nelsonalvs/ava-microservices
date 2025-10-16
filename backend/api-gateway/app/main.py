from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# Configuração dos serviços
# Configuração dos serviços
SERVICES = {
    'auth': 'http://localhost:8001',
    'recommendation': 'http://localhost:8002'  # ✅ Agora está rodando!
}

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'API Gateway do AVA',
        'services': list(SERVICES.keys())
    })

@app.route('/auth/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/auth/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth_proxy(path=''):
    """Roteia requisições para o Auth Service"""
    return proxy_request('auth', path)

@app.route('/recommendation/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/recommendation/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def recommendation_proxy(path=''):
    """Roteia requisições para o Recommendation Service"""
    return proxy_request('recommendation', path)


def proxy_request(service_name, path):
    """Faz proxy da requisição para o serviço específico"""
    if service_name not in SERVICES:
        return jsonify({'error': f'Serviço {service_name} não encontrado'}), 404
    
    service_url = SERVICES[service_name]
    
    # Constrói a URL correta
    if path:
        target_url = f"{service_url}/{path}"
    else:
        target_url = service_url
    
    logger.info(f"Roteando para {target_url}")
    
    try:
        # Forward da requisição
        if request.method == 'GET':
            response = requests.get(
                target_url,
                params=request.args,
                headers={key: value for key, value in request.headers if key != 'Host'}
            )
        elif request.method == 'POST':
            response = requests.post(
                target_url,
                json=request.get_json(silent=True) or {},
                headers={key: value for key, value in request.headers if key != 'Host'}
            )
        else:
            return jsonify({'error': 'Método não suportado'}), 405
        
        # Retorna a resposta do serviço
        return (response.content, response.status_code, response.headers.items())
    
    except requests.exceptions.ConnectionError:
        logger.error(f"Serviço {service_name} não está respondendo: {target_url}")
        return jsonify({'error': f'Serviço {service_name} indisponível'}), 503
    except Exception as e:
        logger.error(f"Erro no gateway: {str(e)}")
        return jsonify({'error': 'Erro interno do gateway'}), 500
    


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

if __name__ == '__main__':
    print("🚀 API Gateway iniciando na porta 8000...")
    app.run(debug=True, host='0.0.0.0', port=8000)
