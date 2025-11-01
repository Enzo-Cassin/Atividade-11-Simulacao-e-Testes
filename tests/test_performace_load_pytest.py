import pytest
import gevent
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.runners import LocalRunner
from locustfile_para_mock import ECommerceUser # Importa sua classe do locustfile

# --- Configuração das Metas (do seu plano) ---
META_P95_MS = 500
META_REQ_S = 2000 # CUIDADO: Esta meta é alta para um mock_server local
META_DISPONIBILIDADE = 0.999

# --- Configuração da Simulação ---
HOST = "http://127.0.0.1:5000"
SIMULATION_USERS = 100 # Comece com 100 usuários, não 10.000
SPAWN_RATE = 10
RUN_TIME_SECONDS = 30 # Roda por 30 segundos

@pytest.fixture
def locust_environment():
    """
    Este "fixture" do pytest cria um ambiente Locust programático 
    antes do teste começar e o destrói depois.
    """
    env = Environment(user_classes=[ECommerceUser])
    env.host = HOST
    
    # Cria um 'runner' local (não distribuído)
    runner = LocalRunner(env)
    
    # Não precisamos iniciar o printer ou history manualmente,
    # o runner e o env cuidam da coleta de stats (env.stats).
    
    # Inicia a simulação
    runner.start(SIMULATION_USERS, spawn_rate=SPAWN_RATE)
    
    # Cria um "timer" para parar o teste após RUN_TIME_SECONDS
    gevent.spawn_later(RUN_TIME_SECONDS, lambda: runner.quit())
    
    # Aguarda o 'runner' parar completamente
    runner.greenlet.join()
    
    # Retorna as estatísticas finais para o teste
    yield env.stats

def test_black_friday_performace_load_test(locust_environment):
    """
    Executa o teste de carga e verifica as métricas.
    """
    stats = locust_environment
    
    # --- Verificação das Metas ---
    
    # Coleta as estatísticas totais (agregadas)
    total_stats = stats.total
    
    print(f"\n--- Resultados Finais do Teste ---")
    print(f"Total de Requests: {total_stats.num_requests}")
    print(f"Total de Falhas: {total_stats.num_failures}")
    print(f"Throughput (req/s): {total_stats.total_rps:.2f}")
    print(f"Tempo de Resposta P95: {total_stats.get_response_time_percentile(0.95):.0f} ms")
    
    # Meta 1: Disponibilidade
    taxa_de_falha = total_stats.fail_ratio
    assert taxa_de_falha < (1.0 - META_DISPONIBILIDADE), \
        f"Taxa de falha {taxa_de_falha*100:.2f}% foi >= meta de {(1.0 - META_DISPONIBILIDADE)*100:.2f}%"

    # Meta 2: Teste de Desempenho (P95)
    p95 = total_stats.get_response_time_percentile(0.95)
    assert p95 < META_P95_MS, \
        f"P95 ({p95:.0f} ms) foi >= meta de {META_P95_MS} ms"

    # Meta 3: Teste de Carga (Throughput)
    # NOTA: O mock_server rodando na sua máquina provavelmente não alcançará 
    # 2000 req/s. Ajuste a meta META_REQ_S ou a simulação.
    rps = total_stats.total_rps
    assert rps > META_REQ_S, \
        f"Throughput ({rps:.2f} req/s) foi <= meta de {META_REQ_S} req/s"