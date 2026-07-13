# Plano de Rollback — Go-Live Assistente de IA (NovaTech)

**Exercício 3.1 — Delivery Manager | Harness Engineering**

Complementa os critérios de go-live ([01-criterios-golive.md](01-criterios-golive.md)). Define quando desligar, quem decide, o que fazer e quem é avisado — sem depender de "avaliar a situação" em tempo real.

---

## Tabela de Triggers

| Trigger | Limite objetivo | Quem decide | Ação | Comunicação |
|---|---|---|---|---|
| **Qualidade — taxa de erro reportada** | >15% das respostas marcadas como incorretas pelos atendentes (ou pela verificação automática de fonte inexistente) em uma janela de 2 horas | Product Specialist | Desativar o bot no Teams para novas perguntas; reverter atendimento para 100% humano (os 5 atendentes-piloto) | Avisar Delivery Manager e Tech Lead em até 10 min via canal Teams dedicado "#novatech-ai-incidentes" |
| **Qualidade — respostas sem fonte** | Pico de >10% de respostas retornadas sem `source_document` válido (falha do structured output) em 30 minutos | Tech Lead | Congelar o endpoint de query (retornar fallback "indisponível temporariamente"); reverter deploy para a última versão estável do endpoint | Avisar Product Specialist e Delivery Manager em até 15 min |
| **Segurança / dados sensíveis** | Qualquer ocorrência confirmada de dado sensível de atendente ou cliente em log, resposta ou output do bot (mesmo 1 ocorrência) | Tech Lead (com autoridade de kill switch imediato — ver abaixo) | Desligar o bot no Teams imediatamente; revogar acesso do módulo/endpoint envolvido; iniciar rotina de purge do log afetado | Avisar Delivery Manager, Product Specialist e responsável de segurança/compliance em até 5 min, independentemente do horário |
| **Disponibilidade — endpoint fora do ar** | Indisponibilidade do endpoint de query por >10 minutos contínuos (falha de timeout/circuit breaker não conteve a queda) | Tech Lead | Reverter atendimento para 100% humano; congelar ingestão/reindexação em andamento até estabilizar | Avisar Delivery Manager em até 10 min; avisar os 5 atendentes-piloto via Teams imediatamente após a decisão |
| **Governança — fila de HITL travada** | Fila de revisão humana (HITL) com mais de 3 respostas aguardando por >10 min cada (SLA de 5 min já estourado em série) | Product Specialist | Bloquear novas perguntas de tema sensível/baixa confiança até normalizar a fila; acionar revisor backup nomeado | Avisar Delivery Manager em até 10 min |

---

## Kill Switch Imediato (sem deliberação)

**Critério:** vazamento confirmado de dado sensível (de atendente ou cliente) em qualquer canal — log, resposta do bot, ou output de módulo gerado por IA. Esta é a única categoria em que a gravidade dispensa reunião ou confirmação de outra pessoa antes de agir.

**Quem aciona sozinho:** **Tech Lead**. Não precisa de aprovação do Delivery Manager ou do Product Specialist para desligar — a decisão é tomada e comunicada em seguida, não antes.

**Ação imediata:** desligar o bot no Teams, revogar acesso do componente envolvido, e notificar Delivery Manager + Product Specialist + responsável de segurança em até 5 minutos.

**Justificativa:** todos os outros triggers toleram uma janela de minutos para decisão porque o dano é reversível ou contido (respostas erradas, indisponibilidade). Vazamento de dado sensível já é um dano consumado no momento em que é detectado — cada minuto adicional de exposição piora o incidente, não a decisão de desligar.
