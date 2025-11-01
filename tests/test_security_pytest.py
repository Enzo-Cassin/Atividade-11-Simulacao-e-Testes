import pytest
import requests
import time

# Configuração do Teste
TARGET_HOST = "http://127.0.0.1:5000"
ENDPOINT = "/api/login"
LIMIT = 100 # Meta: 100 req/min/IP

@pytest.fixture(scope="module")
def session():
    """Cria uma sessão de requests para reutilizar a conexão."""
    return requests.Session()

def test_rate_limit_blocking(session):
    """
    Verifica se o servidor bloqueia com 429 Too Many Requests
    exatamente após o limite de 100 requisições.
    """
    url = f"{TARGET_HOST}{ENDPOINT}"
    
    print(f"\n[INFO] Enviando {LIMIT} requisições (devem passar)...")
    
    start_time = time.time()
    
    # 1. Envia requisições ATÉ o limite (100)
    for i in range(LIMIT):
        try:
            response = session.get(url)
            assert response.status_code == 200, f"Request #{i+1} falhou inesperadamente com {response.status_code}"
            
            # Garante que o teste não demore mais de 1 min
            elapsed = time.time() - start_time
            assert elapsed < 60, "O teste demorou mais de 60s para atingir o limite"
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Erro de conexão no request #{i+1}: {e}")

    print(f"\n[INFO] Limite de {LIMIT} requisições atingido.")
    print(f"[INFO] Enviando request #{LIMIT + 1} (deve falhar com 429)...")
    
    # 2. Envia a requisição QUE DEVE FALHAR (101)
    final_response = session.get(url)
    
    # 3. Verifica se falhou com o código correto
    assert final_response.status_code == 429, \
        f"Servidor respondeu {final_response.status_code} em vez de 429 Too Many Requests"

    print(f"[PASS] Servidor bloqueou com 429 como esperado.")