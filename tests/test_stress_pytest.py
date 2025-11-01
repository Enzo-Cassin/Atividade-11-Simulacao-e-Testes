import pytest
import gevent
from locust.env import Environment
from locust.runners import LocalRunner
from locustfile_para_mock import ECommerceUser # Importa sua classe do locustfile

# --- Configuração das Metas ---
# Meta: Sobreviver a 15.000 usuários (Meta da atividade)
# Usaremos 5% de falha como o "ponto de quebra"
BREAKING_POINT_FAILURE_RATE = 0.05 

# --- Configuração da Simulação ---
HOST = "http://127.0.0.1:5000"
# CUIDADO: 15.000 usuários podem exigir muitos recursos da sua máquina local.
# Comece com um valor menor (ex: 1500) e aumente se funcionar.
STRESS_USERS = 1500 # Valor reduzido para teste local (Meta real: 15000)
SPAWN_RATE = 100
RUN_TIME_SECONDS = 60 # Roda por 1 minuto

@pytest.fixture
def locust_stress_environment():
    """
    Cria um ambiente Locust, roda a simulação de estresse e 
    retorna as estatísticas.
    """
    env = Environment(user_classes=[ECommerceUser])
    env.host = HOST
    runner = LocalRunner(env)
    
    runner.start(STRESS_USERS, spawn_rate=SPAWN_RATE)
    
    # Roda por 60 segundos
    gevent.spawn_later(RUN_TIME_SECONDS, lambda: runner.quit())
    runner.greenlet.join()
    
    yield env.stats

def test_stress_target(locust_stress_environment):
    """
    Verifica se o sistema NÃO quebrou (taxa de falha < 5%) 
    ao atingir a carga de 15.000 usuários.
    """
    stats = locust_stress_environment
    total_stats = stats.total
    
    print(f"\n--- Resultados Finais do Teste de Estresse ({STRESS_USERS} usuários) ---")
    print(f"Total de Requests: {total_stats.num_requests}")
    print(f"Total de Falhas: {total_stats.num_failures}")
    print(f"Taxa de Falha: {total_stats.fail_ratio * 100:.2f}%")

    # Meta Principal: A taxa de falha deve ser MENOR que o ponto de quebra
    assert total_stats.fail_ratio < BREAKING_POINT_FAILURE_RATE, \
        f"Ponto de quebra atingido! Taxa de falha ({total_stats.fail_ratio * 100:.2f}%) foi >= {BREAKING_POINT_FAILURE_RATE * 100}%"
    
    print(f"[PASS] Sistema sobreviveu a {STRESS_USERS} usuários.")