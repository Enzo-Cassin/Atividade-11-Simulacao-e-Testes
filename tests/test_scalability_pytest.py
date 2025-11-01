import pytest
import gevent
import json
import os
from locust.env import Environment
from locust.runners import LocalRunner
from locustfile_para_mock import ECommerceUser

# --- Configuração da Simulação ---
HOST = "http://127.0.0.1:5000"
RUN_TIME_SECONDS = 30
RESULTS_FILE = "scalability_results.json"

# --- Configuração dos Testes ---
BASELINE_USERS = 500  # Carga para N=1 servidor
SCALED_USERS = 1000   # Carga para N=2 servidores (dobro)
META_EFICIENCIA = 0.80 # Meta: > 80%

def _run_locust_test(users, spawn_rate):
    """Função auxiliar para rodar um teste locust e retornar o RPS."""
    env = Environment(user_classes=[ECommerceUser])
    env.host = HOST
    runner = LocalRunner(env)
    runner.start(users, spawn_rate=spawn_rate)
    gevent.spawn_later(RUN_TIME_SECONDS, lambda: runner.quit())
    runner.greenlet.join()
    
    rps = env.stats.total.total_rps
    print(f"\n[INFO] Teste com {users} usuários concluído. Throughput (RPS): {rps:.2f}")
    return rps

# 1. Primeiro Teste: Linha de Base (N=1)
def test_scalability_baseline():
    """
    Roda o teste de linha de base (N=1 servidor) e salva o resultado.
    """
    print(f"\n--- PASSO 1: Executando Teste Baseline ({BASELINE_USERS} usuários) ---")
    throughput_t1 = _run_locust_test(BASELINE_USERS, spawn_rate=BASELINE_USERS)
    
    assert throughput_t1 > 0, "Throughput da linha de base foi 0. O teste falhou."
    
    # Salva o resultado para o próximo teste
    with open(RESULTS_FILE, 'w') as f:
        json.dump({"throughput_t1": throughput_t1}, f)
        
    print(f"[PASS] Resultado T1 ({throughput_t1:.2f} RPS) salvo em {RESULTS_FILE}")

# 2. Segundo Teste: Carga Escalonada (N=2) e Verificação
def test_scalability_scaled_and_assert():
    """
    Roda o teste escalonado (N=2 servidores), lê o resultado N=1
    e calcula a eficiência.
    """
    print(f"\n--- PASSO 2: Executando Teste Escalonado ({SCALED_USERS} usuários) ---")
    
    # Verifica se o arquivo de baseline existe
    if not os.path.exists(RESULTS_FILE):
        pytest.fail(f"Arquivo {RESULTS_FILE} não encontrado. "
                    "Execute 'pytest -v -s test_scalability_baseline.py' primeiro.")
    
    # Carrega o resultado do T1
    with open(RESULTS_FILE, 'r') as f:
        results = json.load(f)
        throughput_t1 = results.get("throughput_t1")

    # Roda o teste N=2
    throughput_t2 = _run_locust_test(SCALED_USERS, spawn_rate=SCALED_USERS)
    assert throughput_t2 > 0, "Throughput escalonado foi 0."
    
    # Calcula a eficiência
    ideal_throughput = throughput_t1 * 2
    eficiencia = throughput_t2 / ideal_throughput
    
    print("\n--- Resultados Finais da Escalabilidade ---")
    print(f"Throughput T1 (N=1): {throughput_t1:.2f} RPS")
    print(f"Throughput T2 (N=2): {throughput_t2:.2f} RPS")
    print(f"Throughput Ideal (T1*2): {ideal_throughput:.2f} RPS")
    print(f"Eficiência Horizontal: {eficiencia * 100:.2f}%")
    
    assert eficiencia > META_EFICIENCIA, \
        f"Eficiência ({eficiencia * 100:.2f}%) foi <= meta de {META_EFICIENCIA * 100}%"
        
    print(f"[PASS] Eficiência atingiu a meta de > {META_EFICIENCIA * 100}%")