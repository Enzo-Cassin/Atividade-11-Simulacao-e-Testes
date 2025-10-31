# Atividade-11-Simulacao-e-Testes

# Plano de Teste Integrado de E-commerce (Black Friday)

## 1. Cenário e Requisitos

Desenvolver um plano de teste completo para um sistema de e-commerce que será lançado na Black Friday.

**Requisitos do Sistema:**
* Suportar 10.000 usuários simultâneos esperados.
* Tempo de resposta < 500ms para 95% das requisições (P95).
* Disponibilidade de 99.9% durante o evento.
* Proteção contra ataques e vazamento de dados.

---

## 2. Tipos de Teste Não Funcionais

### 2.1. Teste de Desempenho

* **Objetivo:** Avaliar a velocidade e responsividade do sistema, garantindo que 95% dos usuários tenham uma experiência rápida.
* **Métrica Obrigatória:** Tempo de resposta P95.
* **Meta Definida:** < 500ms.
* **Estratégia de Execução:**
    1.  Simular uma carga de 10.000 usuários.
    2.  Executar um "Mix de operações" realista (ex: 70% leitura, 20% escrita, 10% relatórios).
    3.  Monitorar a métrica P95 (percentil 95) durante todo o teste.
* **Critério de Aprovação/Reprovação:**
    * **Aprovado:** P95 < 500ms.
    * **Reprovado:** P95 >= 500ms.

### 2.2. Teste de Carga

* **Objetivo:** Verificar como o sistema se comporta sob a carga de pico esperada (Black Friday) e validar a capacidade de processamento (throughput).
* **Métrica Obrigatória:** Throughput sustentado.
* **Meta Definida:** > 2000 req/s.
* **Estratégia de Execução:**
    1.  Simular 10.000 usuários simultâneos.
    2.  Sustentar essa carga por um período definido (ex: 1-2 horas).
    3.  Medir o número de requisições por segundo (throughput) que o sistema consegue manter.
* **Critério de Aprovação/Reprovação:**
    * **Aprovado:** Throughput médio > 2000 req/s com taxa de erro < 0.1%.
    * **Reprovado:** Throughput <= 2000 req/s ou taxa de erro >= 0.1%.

### 2.3. Teste de Estresse

* **Objetivo:** Encontrar o ponto de quebra do sistema aplicando carga além da capacidade planejada.
* **Métrica Obrigatória:** Ponto de quebra (em nº de usuários).
* **Meta Definida:** > 15.000 usuários.
* **Estratégia de Execução:**
    1.  Utilizar um método de "Ramp-up gradual", iniciando com 10.000 usuários.
    2.  Adicionar +1000 usuários a cada 5 minutos até o sistema falhar.
    3.  O "ponto de quebra" é definido quando a taxa de erro excede 5% ou o tempo de resposta cresce exponencialmente.
* **Critério de Aprovação/Reprovação:**
    * **Aprovado:** Ponto de quebra > 15.000 usuários.
    * **Reprovado:** Ponto de quebra <= 15.000 usuários.

### 2.4. Teste de Escalabilidade

* **Objetivo:** Verificar a capacidade do sistema de crescer horizontalmente (adicionar mais servidores) e medir se a performance melhora proporcionalmente.
* **Métrica Obrigatória:** Eficiência horizontal.
* **Meta Definida:** > 80%.
* **Estratégia de Execução:**
    1.  **Baseline (N=1):** Executar um teste de carga com 1 servidor e 5.000 usuários. Registrar o Throughput (T1).
    2.  **Scale Out (N=2):** Executar o mesmo teste com 2 servidores e 10.000 usuários. Registrar o Throughput (T2).
    3.  **Cálculo:** `Eficiência = (T2 / (T1 * 2)) * 100`.
* **Critério de Aprovação/Reprovação:**
    * **Aprovado:** Eficiência horizontal > 80%.
    * **Reprovado:** Eficiência horizontal <= 80%.

### 2.5. Teste de Segurança

* **Objetivo:** Identificar vulnerabilidades e verificar se mecanismos de proteção (como Rate Limit) estão ativos para prevenir abuso.
* **Métrica Obrigatória:** Rate limiting (Limite de requisições por IP).
* **Meta Definida:** 100 req/min/IP.
* **Estratégia de Execução:**
    1.  Criar um script (Python `requests`) que dispare requisições em loop de um único IP para um endpoint (ex: `/login`).
    2.  Verificar se, após 100 requisições em 60 segundos, o sistema retorna o status `HTTP 429 Too Many Requests`.
    3.  Verificar se o acesso é restabelecido após o período de bloqueio.
* **Critério de Aprovação/Reprovação:**
    * **Aprovado:** Sistema bloqueia no limite (100 req/min) e retorna HTTP 429.
    * **Reprovado:** Sistema permite mais de 100 req/min ou falha com outro erro (ex: 500).

---
