# Plano de Observabilidade — Assistente de IA (NovaTech)

**Exercício 3.2 — Delivery Manager | Revisão Crítica de Outputs de IA (aplicada a monitoramento)**

Contexto: assistente (RAG + bot no Teams) recém em produção, usado por atendentes. ~12% das respostas podem sair incorretas (alucinação, doc desatualizado, chunk errado). Respostas trazem `confidence_score` e `source_document`. A NovaTech quer saber semanalmente se o assistente está melhorando ou piorando.

Este plano se apoia no que já foi definido em [01-criterios-golive.md](01-criterios-golive.md) (structured output, HITL, logging) e no que foi identificado no pré-mortem do [03-plano-rollback.md](03-plano-rollback.md) — em especial a falha #2 (detecção passiva de vazamento) e a falha #1 (ninguém monitorando ativamente): este plano corrige essas lacunas ao definir alertas ativos, não apenas dashboards passivos.

---

## 1. Métricas de Uso

| Métrica | Como é medida | Fonte do dado |
|---|---|---|
| Perguntas/dia (volume total e por atendente) | Contagem de requisições ao endpoint de query, agregada por dia | Log de interação (structured output logging) |
| Usuários ativos (atendentes-piloto que fizeram ≥1 pergunta no dia) | Contagem de `user_id` distintos por dia | Log de interação / autenticação do bot no Teams |
| Tempo médio de resposta ponta a ponta (pergunta → resposta entregue ao atendente) | Diferença entre timestamp de recebimento da pergunta e timestamp de entrega da resposta | Log de interação |
| Horário de pico de uso | Distribuição de volume de perguntas por hora do dia | Log de interação, agregação horária |

## 2. Métricas de Qualidade

| Métrica | Como é medida | Fonte do dado |
|---|---|---|
| % de feedback negativo | (respostas marcadas "não ajudou" pelo atendente / total de respostas com feedback) × 100 | Botão de feedback no bot do Teams (👍/👎) |
| Taxa de participação no feedback | (respostas com algum clique 👍 ou 👎 / total de respostas entregues) × 100 — distingue "qualidade melhorou" de "atendentes pararam de reagir" | Botão de feedback no bot do Teams (👍/👎), cruzado com total de respostas do log de interação |
| % de escalações para humano | (perguntas que o atendente encaminhou para um humano ou reformulou manualmente / total de perguntas) × 100 | Log de interação + evento de escalação do bot |
| % de respostas retidas para HITL (baixa confiança ou tema sensível) | (respostas com `confidence_score < 0.6` OU tema sensível / total de respostas) × 100 | Log de HITL (já definido como bloqueante em 01) |
| Distribuição de `confidence_score` (média e % abaixo de 0.6) | Agregação estatística do campo `confidence_score` do structured output | Log de interação |
| Taxa de erro de citação (fonte citada não existe no índice) | (respostas com `source_document` inválido / total) × 100 | Verificação automática de fonte (já bloqueante em 01) |

## 3. Métricas Técnicas

| Métrica | Como é medida | Fonte do dado |
|---|---|---|
| Latência p95 do endpoint de query | Percentil 95 do tempo de resposta do endpoint (excluindo tempo de UI do Teams) | Tracing/logs do endpoint (Application Insights ou equivalente) |
| Taxa de erro/timeout do endpoint | (requisições com erro 5xx ou timeout / total de requisições) × 100 | Logs de infraestrutura do endpoint |
| Disponibilidade (uptime) | % de tempo em que o endpoint respondeu dentro do SLA, medido por health check a cada 1 min | Monitor de health check externo |
| Taxa de falha do circuit breaker (Azure AI Search) | Número de vezes que o circuit breaker abriu por dia | Logs de orquestração (camada 1 do harness) |

## 4. Métricas de Conteúdo

| Métrica | Como é medida | Fonte do dado |
|---|---|---|
| Documentos mais consultados (top 10) | Contagem de `source_document` citado, agregada por documento, por semana | Log de interação |
| Perguntas sem resposta (fallback "não encontrei informação suficiente") | Contagem de respostas em fallback / total de perguntas | Log de interação (já bloqueante em 01: fallback explícito) |
| Documentos nunca consultados (candidatos a desatualizados ou irrelevantes) | Documentos no índice com 0 citações em 30 dias | Cruzamento entre índice do Azure AI Search e log de citações |
| Perguntas recorrentes sem resposta satisfatória (agrupadas por similaridade) | Clusterização semântica de perguntas com feedback negativo ou fallback | Log de interação + processamento semanal (batch) |

---

## Alertas

| # | Gatilho numérico | Janela de tempo | Quem é notificado | Canal |
|---|---|---|---|---|
| 1 | % de feedback negativo > 15% | 24 horas | Product Specialist + Tech Lead | Teams — canal `#novatech-ai-incidentes` |
| 2 | Latência p95 do endpoint > 5 segundos OU taxa de erro/timeout > 5% | 30 minutos | Tech Lead (on-call) | Teams — canal `#novatech-ai-incidentes` + alerta automático (Application Insights) |
| 3 | % de perguntas sem resposta (fallback) > 20% | 24 horas | Product Specialist | Teams — canal `#novatech-ai-observabilidade` |
| 4 | Taxa de participação no feedback cai >30% em relação à média móvel das últimas 4 semanas | 7 dias | Product Specialist | Teams — canal `#novatech-ai-observabilidade` |

**Nota sobre o alerta 4:** protege contra o falso-positivo de "% de feedback negativo caindo" ser lido como melhoria quando, na verdade, os atendentes só pararam de reagir (feedback fatigue). Sem este alerta, uma queda de participação e uma melhoria real de qualidade produzem o mesmo sinal no dashboard — o relatório semanal reportaria "melhorando" quando a taxa real de erro pode estar estável ou pior.

**Nota:** os alertas 1 e 3 usam janela de 24h (adequada a tendência de qualidade/conteúdo); o alerta 2 usa 30 min por ser sintoma técnico agudo que já está coberto como trigger de rollback em [03-plano-rollback.md](03-plano-rollback.md) — este alerta é o sinal antecipado que aciona aquele trigger antes de ele estourar o limite de 10 min de indisponibilidade.

---

## Feedback Loop — do clique do atendente à correção em produção

1. **Sinalização**: o atendente clica 👎 ("não ajudou") na resposta do bot no Teams e, opcionalmente, digita um motivo curto (ex.: "fonte errada", "informação desatualizada").
2. **Registro**: o clique gera um evento de feedback negativo, logado junto com a pergunta, a resposta completa, `source_document`, `confidence_score` e o motivo informado.
3. **Triagem semanal**: o Product Specialist revisa a fila de feedbacks negativos acumulados da semana, classificando cada um em uma categoria: (a) documento desatualizado, (b) chunk incorreto recuperado, (c) alucinação (resposta não sustentada por nenhum chunk), (d) pergunta fora do escopo do assistente.
4. **Ação por categoria**:
   - (a) Documento desatualizado → aciona reindexação pontual do documento específico no Azure AI Search.
   - (b) Chunk incorreto → Tech Lead ajusta parâmetros de recuperação (tamanho de chunk, estratégia de busca) ou adiciona metadado ao documento para melhorar a correspondência.
   - (c) Alucinação → Tech Lead revisa o prompt/instruções do modelo para reforçar "responder apenas com base no chunk recuperado"; casos graves entram no conjunto de teste de regressão já definido como bloqueante em 01.
   - (d) Fora do escopo → não gera correção técnica; registrado como limite conhecido do assistente, comunicado ao atendente-piloto.
5. **Priorização**: perguntas recorrentes (mesmo cluster semântico, ≥3 ocorrências na semana) têm prioridade sobre casos isolados.
6. **Implementação**: a correção (reindexação, ajuste de parâmetro, ajuste de prompt) é aplicada em ambiente de staging.
7. **Validação**: a mesma pergunta que gerou o feedback negativo é reexecutada em staging para confirmar que a resposta melhorou antes de promover a mudança para produção.
8. **Deploy**: a correção validada é promovida para produção dentro do ciclo semanal (fora da janela dos alertas críticos, evitando deploy nas 24h seguintes a um alerta ativo).
9. **Fechamento do ciclo**: o item de feedback é marcado como "resolvido" no registro, e a métrica de % de feedback negativo da semana seguinte é o indicador de que a correção funcionou — se a mesma categoria de erro reaparecer, o ciclo reabre.
