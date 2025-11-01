from flask import Flask, request, jsonify, make_response
import time
import random

app = Flask(__name__)

# --- Simulação do Rate Limit (para o Teste de Segurança) ---
# Usamos um dicionário simples para rastrear os IPs
# (Em um app real, isso seria feito com um banco de dados como Redis)
rate_limit_db = {}
LIMIT_PER_MINUTE = 100 # Meta de 100 req/min/IP

@app.route('/api/login', methods=['GET', 'POST'])
def mock_login():
    """
    Este endpoint simula uma tela de login e aplica um 
    Rate Limit de 100 requisições por minuto por IP.
    """
    # Pega o IP do cliente (no seu teste, será 127.0.0.1)
    ip = request.remote_addr
    
    current_time = time.time()
    
    if ip not in rate_limit_db:
        # Primeira requisição deste IP
        rate_limit_db[ip] = {
            "count": 1,
            "window_start": current_time
        }
    else:
        # IP já conhecido, verifica a janela de tempo
        data = rate_limit_db[ip]
        time_passed = current_time - data["window_start"]
        
        if time_passed > 60:
            # Janela de 1 minuto passou, reseta a contagem
            data["count"] = 1
            data["window_start"] = current_time
        else:
            # Ainda dentro da janela, incrementa o contador
            data["count"] += 1
            
    # Verifica se o limite foi excedido
    if rate_limit_db[ip]["count"] > LIMIT_PER_MINUTE:
        
        # RETORNA O ERRO 429 (Too Many Requests)
        print(f"IP {ip} atingiu o limite! (Request #{rate_limit_db[ip]['count']})")
        response = make_response(jsonify(error="Too Many Requests"), 429)
        response.headers['Retry-After'] = 60 # Informa quando tentar de novo
        return response

    # Se não atingiu o limite, retorna 200 OK
    print(f"IP {ip} fez request (Contagem: {rate_limit_db[ip]['count']})")
    return jsonify(message="Login OK"), 200


# --- Endpoints para o Locust (Teste de Carga) ---

@app.route('/produto/<int:product_id>', methods=['GET'])
def mock_view_product(product_id):
    """ Simula a visualização de um produto """
    # Simula um tempo de resposta de banco de dados (100-300ms)
    time.sleep(random.uniform(0.1, 0.3))
    return jsonify(product_id=product_id, name=f"Produto {product_id}"), 200

@app.route('/categoria/<string:category_name>', methods=['GET'])
def mock_view_category(category_name):
    """ Simula a visualização de uma categoria """
    # Simula um tempo de resposta mais rápido (50-100ms)
    time.sleep(random.uniform(0.05, 0.1))
    return jsonify(category=category_name, items=[1, 2, 3]), 200

@app.route('/api/carrinho/add', methods=['POST'])
def mock_add_to_cart():
    """ Simula uma operação de escrita (adição ao carrinho) """
    # Simula uma operação mais lenta (200-500ms)
    time.sleep(random.uniform(0.2, 0.5))
    return jsonify(status="item_added", items_in_cart=random.randint(1, 5)), 201

@app.route('/checkout', methods=['GET'])
def mock_checkout():
    """ Simula a visita à página de checkout """
    time.sleep(random.uniform(0.1, 0.2))
    return jsonify(message="Pagina de checkout"), 200

# --- Rota principal ---

@app.route('/')
def home():
    return "Servidor Falso (Mock Server) está no ar! Use os endpoints /produto, /categoria, etc."

if __name__ == '__main__':
    # Roda o servidor Flask na porta 5000
    app.run(debug=True, host='127.0.0.1', port=5000)