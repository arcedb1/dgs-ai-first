# Template — Checklist de Validation Gates
**Projeto:** NovaTech Assistant
**Uso:** copiar este bloco para o item do módulo/spec no board (Azure DevOps ou Cowork) a cada transição de etapa. Preencher `[x]`, registrar aprovador e data.

---

## Gate 1 — Spec → Plan
*Antes de o Tech Lead começar o `plan.md`, alguém precisa confirmar que o `requirements.md` está pronto para virar decisão técnica.*

**Quem aprova**
Product Specialist (dono da spec)

**O que verifica**
- [ ] Outcomes descrevem resultado para o usuário/negócio, não feature técnica
- [ ] Scope boundaries explicitam o que este módulo cobre e o que fica fora
- [ ] Toda prior decision referenciada existe como ADR em `/docs/adr/`
- [ ] Cada verification criterion é testável (o QA consegue escrever um caso de teste a partir dele, sem perguntar nada)
- [ ] Termos de domínio usados batem com a linguagem ubíqua definida (sem ambiguidade tipo "Gold" = tier vs. metal)
- [ ] O artefato está marcado como rascunho até a aprovação final
- [ ] Há evidência mínima disponível para a aprovação (artefato revisado, mudanças listadas, riscos conhecidos)
- [ ] Dados sensíveis, segredos ou informações internas não foram compartilhados sem redaction
- [ ] Em caso de reprovação, o item segue o plano de rollback/correção e não avança para a próxima etapa

**Quanto tempo tem**
1 dia útil, a contar do momento em que a spec entra em "Em Revisão" no board

**O que acontece se reprovar**
Spec volta para "Rascunho" no board. PS registra os ajustes necessários como comentário no `requirements.md`. Tech Lead não inicia o `plan.md` até nova aprovação. PS tem novo ciclo de 1 dia útil para resubmeter.

**Registro:** Aprovado por ______________ em ___/___/____

---

## Gate 2 — Tasks → Implement
*Antes de o Dev começar a codar, alguém precisa confirmar que as tasks geradas por IA fazem sentido e cobrem o plano.*

**Quem aprova**
Tech Lead

**O que verifica**
- [ ] Cada task é atômica — pode ser implementada e testada de forma independente
- [ ] Critérios de aceite são verificáveis (não é "funcionar corretamente")
- [ ] Dependências entre tasks estão mapeadas e na ordem certa
- [ ] As tasks juntas cobrem 100% do escopo do `plan.md` (nada ficou de fora)
- [ ] Estimativas (P/M/G) são plausíveis dado o histórico do time
- [ ] O `tasks.md` está marcado como rascunho até aprovação final
- [ ] Há evidência mínima disponível para aprovação (tarefas executáveis, riscos mapeados, dependências claras)
- [ ] Não há uso de dados sensíveis sem redaction e sem autorização

**Quanto tempo tem**
4 horas úteis a partir do momento em que o `tasks.md` é gerado (gate rápido — não pode virar fila)

**O que acontece se reprovar**
TL comenta task a task diretamente no `tasks.md`. As tasks reprovadas voltam para ajuste do Dev; as tasks já aprovadas no mesmo arquivo podem seguir para implementação sem esperar as demais.

**Registro:** Aprovado por ______________ em ___/___/____

---

## Gate 3 — Code → Merge
*Antes do merge, um humano precisa revisar o que o agente (Copilot) gerou — o Dev não se auto-aprova.*

**Quem aprova**
Tech Lead (code review); PR exige no mínimo 1 approval

**O que verifica**
- [ ] Código segue o AGENTS.md e as skills aplicáveis (Foundation/Domain/Artifact)
- [ ] Nenhum segredo/credencial hardcoded no código
- [ ] Testes unitários e de integração passam localmente e no CI
- [ ] O Dev revisou criticamente o output do Copilot (não é "aceitar tudo que a IA sugeriu")
- [ ] `docs/pull-requests/PR-NNNN.md` documenta objetivo, mudanças e este checklist preenchido
- [ ] Há evidência mínima para merge (diff revisado, testes executados, riscos conhecidos)
- [ ] O PR não avança sem aprovação humana válida e sem resposta aos comentários críticos
- [ ] O rollback/correção está definido caso o merge gere regressão ou falha

**Quanto tempo tem**
1 dia útil (ou 4 horas se o PR estiver marcado como urgente/bloqueante)

**O que acontece se reprovar**
PR volta com comentários de review. Dev corrige e resubmete. O merge fica bloqueado até haver 1 approval válido — sem exceção, mesmo sob pressão de prazo.

**Registro:** Aprovado por ______________ em ___/___/____

---

## Gate 4 — Tests → Deploy
*Antes do deploy, alguém precisa confirmar que os testes gerados por IA são suficientes, não só que existem.*

**Quem aprova**
QA valida a suficiência dos testes; Tech Lead aprova o deploy em seguida

**O que verifica**
- [ ] Cobertura mínima de 80% de linhas atingida
- [ ] Todo verification criterion do `requirements.md` tem ao menos 1 teste correspondente
- [ ] Cenários de robustez de IA cobertos (prompt injection básico, pergunta ambígua, idioma diferente)
- [ ] Nenhum teste depende de serviço real ou de ordem de execução (mocks/fixtures conforme Testing Standards)
- [ ] QA registra sign-off explícito no board (Cowork) antes do TL aprovar o deploy
- [ ] Há evidência mínima para aprovação (resultados dos testes, gaps conhecidos, risco residual documentado)
- [ ] O deploy fica bloqueado se houver risco crítico não mitigado
- [ ] O plano de rollback está disponível e alinhado com a contingência do fluxo

**Quanto tempo tem**
1 dia útil antes da janela de deploy planejada

**O que acontece se reprovar**
Deploy fica bloqueado. QA lista os gaps de cobertura/cenário. Dev complementa apenas os testes faltantes (não reabre o código todo). Novo ciclo de validação do QA antes de reapresentar ao TL.

**Registro QA:** Aprovado por ______________ em ___/___/____
**Registro deploy (TL):** Aprovado por ______________ em ___/___/____

---

## Resumo rápido (para consulta)

| Gate | Quem aprova | Quanto tempo tem | O que acontece se reprovar |
|---|---|---|---|
| 1. Spec → Plan | Product Specialist | 1 dia útil | Spec volta a "Rascunho"; TL não inicia o plan |
| 2. Tasks → Implement | Tech Lead | 4 horas úteis | Tasks reprovadas voltam para ajuste; aprovadas seguem |
| 3. Code → Merge | Tech Lead (1 approval) | 1 dia útil | PR bloqueado até correção e nova approval |
| 4. Tests → Deploy | QA (testes) + Tech Lead (deploy) | 1 dia útil | Deploy bloqueado; só os testes com gap |

### Métricas e governança adicional
- Tempo médio de revisão por gate
- Taxa de retrabalho ou reprovação
- Número de artefatos reprovados
- Tempo de resposta do assistente
- Custo por ciclo ou por entrega