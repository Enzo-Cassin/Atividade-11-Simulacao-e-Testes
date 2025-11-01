# Relatório de Execução dos Testes Não Funcionais

Este relatório resume os resultados da execução automatizada dos testes de performance (`pytest` + `locust`) contra o `mock_server`.

## Resumo Geral

| Testes Executados | Aprovados | Reprovados |
| :--- | :---: | :---: |
| 5 | 4 | 1 |

**Tempo Total de Execução:** `151.93s (0:02:31)`

---

## Análise Detalhada dos Testes

### 1. Teste de Desempenho e Carga (`test_performa_load_pytest.py`)

Este teste simula a carga da Black Friday (10.000 usuários) e verifica duas metas: P95 (Desempenho) e Throughput (Carga).

* **Status:** **REPROVADO (FAILED)**

#### Métricas Coletadas:
* **Total de Requests:** 1196
* **Total de Falhas:** 0
* **Tempo de Resposta P95:** 390 ms
* **Throughput (req/s):** 40.27

### Metas
**Aprovado** no de **Desempenho** (P95 de 390ms < 500ms)<br>
**Reprovado** no requisito de **Carga**.

* `AssertionError: Throughput (40.27 req/s) foi <= meta de 2000 req/s`

*(**Observação:** Como esperado, o `mock_server` rodando em localhost não conseguiu atingir a meta de 2000 req/s. O teste funcional falhou, o que está correto para os parâmetros definidos.)*

---

### 2. Teste de Escalabilidade (`test_scalability_pytest.py`)

Este teste foi dividido em duas etapas para medir a eficiência horizontal.

* **Status:** **APROVADO (PASSED)**

#### Métricas Coletadas:
* **Throughput T1 (N=1):** 228.97 RPS
* **Throughput T2 (N=2):** 386.24 RPS
* **Throughput Ideal (T1*2):** 457.94 RPS
* **Eficiência Horizontal:** **84.34%**

#### Análise:
O resultado de 84.34% é **maior** que a meta de 80%. O teste foi aprovado.

---

### 3. Teste de Segurança (`test_security_pytest.py`)

Este teste verificou se o `mock_server` aplica corretamente o Rate Limiting.

* **Status:** **APROVADO (PASSED)**

#### Análise:
* `[PASS] Servidor bloqueou com 429 como esperado.`

O servidor permitiu as 100 primeiras requisições (Status 200) e bloqueou a 101ª (Status 429), conforme a meta.

---

### 4. Teste de Estresse (`test_stress_pytest.py`)

Este teste verificou se o sistema sobreviveu a uma carga de 1.500 usuários (valor ajustado para o `mock_server`).

* **Status:** **APROVADO (PASSED)**

#### Métricas Coletadas:
* **Usuários Simulados:** 1500
* **Total de Falhas:** 0
* **Taxa de Falha:** 0.00%

#### Análise:
* `[PASS] Sistema sobreviveu a 1500 usuários.`

O sistema manteve uma taxa de falha de 0.00%, passando no teste de estresse.