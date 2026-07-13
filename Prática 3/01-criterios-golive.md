# Critérios de Go-Live — Harness de Governança (NovaTech AI Assistant)

**Exercício 3.1 — Delivery Manager | Harness Engineering**

Contexto: assistente de IA (RAG + bot no Teams) da NovaTech em staging, com 5 atendentes-piloto. Demo para a diretoria em 2 semanas.

Problemas conhecidos:
- 12% de respostas incorretas (alucinação, documento desatualizado, chunk errado).
- Respostas em texto livre, sem garantia de campos obrigatórios (fonte, confiança).
- Um módulo gerado por IA violou o AGENTS.md (sem Zod, logou dados sensíveis do atendente).
- Cobertura de testes ~75%.

---

## 1. Tool Orchestration

| Critério | Classificação | Justificativa |
|---|---|---|
| Endpoint de query com timeout e retry definidos para chamadas ao Azure AI Search | BLOQUEANTE | Sem timeout, uma falha de busca trava o atendente indefinidamente — risco operacional direto no piloto |
| Fallback explícito quando o retrieval não retorna chunks relevantes (ex.: "não encontrei informação suficiente" em vez de forçar resposta) | BLOQUEANTE | É a causa raiz de parte da alucinação — modelo sem chunk relevante ainda tenta responder |
| Orquestração entre bot do Teams e endpoint com circuit breaker (se endpoint cair, bot informa indisponibilidade) | BLOQUEANTE | 5 atendentes-piloto dependem disso; silêncio ou erro cru quebra a confiança na demo |
| Reprocessamento automático de documentos desatualizados (pipeline de re-indexação agendada) | DESEJÁVEL | Resolve "documento desatualizado", mas dá para mitigar manualmente por 2 semanas com uma reindexação pontual antes da demo |
| Orquestração multi-agente (ex.: agente separado para validar resposta antes de enviar) | DESEJÁVEL | Melhoria de qualidade, mas HITL (camada 4) já cobre o risco crítico no curto prazo |

## 2. Verification Loops

| Critério | Classificação | Justificativa |
|---|---|---|
| **Structured output obrigatório**: resposta do modelo DEVE ser JSON validado por schema (`answer`, `source_document`, `confidence_score`), com rejeição programática (retry ou fallback) de qualquer resposta fora do formato | BLOQUEANTE | Resolve diretamente o problema de "resposta sem fonte" — é o requisito central desta fase e mitigável em código, não em prompt |
| Verificação automática de que `source_document` citado existe de fato no índice (anti-alucinação de fonte) | BLOQUEANTE | Sem isso, o modelo pode "citar" um documento inexistente — pior que não citar nada |
| Teste automatizado de regressão sobre os 12% de casos de erro conhecidos (hallucination/doc desatualizado/chunk errado), rodando antes de cada deploy | BLOQUEANTE | Já sabemos que essas falhas existem; ir ao ar sem monitorá-las é repetir o erro conhecido |
| Elevar cobertura de testes de integração de 75% para 90%+ | DESEJÁVEL | Direção correta, mas perseguir 15 p.p. em 2 semanas é troca ruim por foco nos casos conhecidos de falha acima |
| Verificação semântica automática (LLM-as-judge) de coerência resposta/fonte | DESEJÁVEL | Adiciona uma segunda camada de qualidade, mas HITL cobre o risco imediato de baixa confiança |

## 3. Context & Memory

| Critério | Classificação | Justificativa |
|---|---|---|
| Cada resposta referencia a versão/data de indexação do documento fonte (rastreabilidade) | BLOQUEANTE | Sem isso não dá para diagnosticar "documento desatualizado" nem confiar na citação exigida pelo structured output |
| Sessão do atendente no Teams não vaza contexto entre conversas de atendentes diferentes (isolamento de memória por sessão) | BLOQUEANTE | Vazamento de contexto entre atendentes é risco de dado sensível, agravado pelo incidente do módulo de feedback |
| Memória de conversa persistente entre turnos dentro da mesma sessão do atendente | DESEJÁVEL | Staging já funciona por pergunta única; multi-turno é melhoria de UX, não risco de governança |
| Cache de embeddings/chunks para reduzir latência | DESEJÁVEL | Otimização de performance, sem impacto em confiabilidade ou risco |

## 4. Guardrails (inclui Human-in-the-Loop)

| Critério | Classificação | Justificativa |
|---|---|---|
| **HITL obrigatório**: toda resposta com `confidence_score < 0.6` **OU** classificada em tema sensível (ex.: segurança, dados de cliente, decisão financeira) é retida e enviada para revisão humana antes de chegar ao atendente-piloto | BLOQUEANTE | É o mecanismo definido nesta fase para conter os 12% de erro sem bloquear 100% do fluxo — risco maior de dano é justamente em tema sensível com baixa confiança |
| Revisão e correção do módulo de feedback que violou o AGENTS.md (adicionar validação Zod, remover log de dado sensível de atendente) | BLOQUEANTE | Violação de guardrail já identificada e com exposição de dado sensível — não pode ir ao ar como está |
| Todo código gerado por IA (Copilot) passa por revisão humana antes de merge, validando aderência ao AGENTS.md | BLOQUEANTE | O incidente do módulo de feedback mostra que geração por IA sem revisão já causou violação real — repetir o padrão é risco conhecido e aceito |
| Guardrails de produto (DEVE/NÃO DEVE do Product Specialist) implementados como validação automática (não só documentação) | BLOQUEANTE | Guardrail que só existe em markdown não impede nada em runtime — precisa virar checagem de código/prompt |
| Rate limiting / limite de perguntas por atendente por minuto | DESEJÁVEL | Reduz risco de abuso ou custo, mas não é bloqueio de confiabilidade para uma demo com 5 pilotos |
| Guardrail de conteúdo tóxico/PII na pergunta de entrada (não só na saída) | DESEJÁVEL | Redundante no curto prazo dado o público controlado (5 atendentes internos); vira bloqueante quando abrir para mais usuários |

### Capacidade Operacional do HITL

O critério de HITL (acima) define **quando** a revisão humana é acionada, mas não basta — sem capacidade operacional definida, a fila de revisão pode travar silenciosamente. Este detalhamento é bloqueante e complementa o critério de HITL da tabela acima.

| Elemento | Definição concreta |
|---|---|
| **Responsável primário** | Escala fixa de 2 revisores humanos por turno (ex.: Product Specialist + 1 atendente sênior), nomeados explicitamente — não "o time" genérico |
| **SLA de revisão** | 5 minutos durante o piloto/demo. Se não revisado em 5 min, aciona escalonamento automático |
| **Escalonamento (revisor indisponível)** | Após 5 min sem resposta → notificação automática (ex.: Teams/e-mail) para revisor backup. Após 10 min sem nenhum revisor → resposta é bloqueada e o atendente recebe mensagem padrão: *"Não foi possível validar esta resposta agora, por favor tente novamente em instantes ou contate [canal de suporte]"* — a resposta nunca segue sem revisão por timeout |
| **Cobertura de disponibilidade** | Antes da demo, confirmar explicitamente que os revisores nomeados estão de fato disponíveis nesse período (não estão de férias/alocados em outra prioridade) |
| **Registro da decisão humana** | Toda decisão de HITL (aprovado/rejeitado/editado) é logada com timestamp e identificação do revisor — alimenta a observability da camada 5 |

**Trade-off em aberto:** o timeout de bloqueio (10 min) prioriza segurança sobre disponibilidade — durante a demo ao vivo isso pode gerar uma resposta "bloqueada" visível para a diretoria se o SLA falhar. Recomenda-se um revisor dedicado de plantão, sem outras tarefas, especificamente na janela da demonstração.

## 5. Observability

| Critério | Classificação | Justificativa |
|---|---|---|
| Log de toda interação (pergunta, resposta, `confidence_score`, se passou por HITL, decisão humana) | BLOQUEANTE | Sem isso não há como auditar a demo, medir taxa de erro real, nem investigar incidente como o do módulo de feedback |
| Dashboard/alerta quando taxa de respostas retidas para HITL ou taxa de baixa confiança ultrapassa um limiar (ex.: >20% das perguntas) | BLOQUEANTE | Sinal direto de que o sistema está degradado — é também o gatilho do plano de rollback |
| Máscara/redação de dados sensíveis do atendente nos logs | BLOQUEANTE | Consequência direta do incidente já identificado — logar dado sensível de novo é repetir a falha |
| Dashboard executivo de métricas de negócio (nº de perguntas respondidas, satisfação) para a diretoria | DESEJÁVEL | Bom para a demo, mas é apresentação, não controle de risco — pode ser montado na véspera |
| Tracing distribuído completo (latência por etapa do pipeline) | DESEJÁVEL | Otimização operacional futura, não crítico para uma demo controlada com 5 usuários |

---

## Resumo: o que impede o go-live hoje

1. **Structured output não existe** — respostas em texto livre sem garantia de `source_document`/`confidence_score` é o bloqueio mais urgente, pois sem ele o HITL (que depende de `confidence_score`) nem pode ser implementado.
2. **HITL não está implementado** — não há hoje nenhum ponto de revisão humana antes de a resposta chegar ao atendente, apesar de já se saber que 12% das respostas estão erradas.
3. **Módulo de feedback com violação de guardrail em produção-staging** — sem Zod e logando dado sensível; precisa ser corrigido e revisado antes de qualquer avanço.
4. **Sem verificação de que a fonte citada existe de fato** — abre espaço para "alucinação de citação", pior que a ausência de fonte.
5. **Sem logging/observability de confiança e decisões HITL** — impede validar se os bloqueantes acima estão funcionando na prática, inclusive durante a própria demo.

Com foco nesses 5 pontos (não nos 90% de cobertura de teste, nem em multi-agente), o time tem uma rota realista para os itens bloqueantes em 2 semanas.
