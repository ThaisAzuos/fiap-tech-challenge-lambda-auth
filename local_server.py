"""
Servidor local que simula o AWS Lambda + API Gateway para desenvolvimento.
Uso: python local_server.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Lê a chave privada do arquivo e injeta como variável de ambiente
# (jwt_generator.py espera JWT_PRIVATE_KEY como env var)
key_path = os.environ.get('JWT_PRIVATE_KEY_PATH')
if key_path and os.path.exists(key_path):
    with open(key_path, 'r') as f:
        os.environ['JWT_PRIVATE_KEY'] = f.read()
    print(f"Chave privada carregada de: {key_path}")
elif not os.environ.get('JWT_PRIVATE_KEY'):
    print("AVISO: JWT_PRIVATE_KEY e JWT_PRIVATE_KEY_PATH não definidos")

import json
from flask import Flask, request, jsonify
from handler import lambda_handler

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    body = request.get_json()
    event = {'body': body}
    result = lambda_handler(event, {})
    status_code = result.get('statusCode', 500)
    body_content = result.get('body', '{}')
    if isinstance(body_content, str):
        body_content = json.loads(body_content)
    return jsonify(body_content), status_code

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'UP'}), 200

if __name__ == '__main__':
    print("Lambda local rodando em http://localhost:9000")
    print("Endpoint: POST http://localhost:9000/authenticate")
    app.run(host='0.0.0.0', port=9000, debug=False)
