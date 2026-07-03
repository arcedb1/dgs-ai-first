# Fluxo de Trabalho AI First — Projeto NovaTech Assistant

**Autor:** Delivery Manager
**Ciclo mapeado:** Spec → Plan → Tasks → Implement → Review → Deploy
**Ferramentas do projeto:** GitHub Copilot, Claude (chat), Claude Cowork, Claude Design, Azure DevOps, GitHub

---

## 1. Visão geral do fluxo

O time é AI First, não AI Only: em cada etapa um agente de IA produz o rascunho e um humano específico decide se ele avança. A regra geral de alocação de ferramentas é:

- **Claude (chat)** — raciocínio, redação de specs/planos/tasks, análise crítica. Usado por todos os papéis, em todas as etapas.
- **GitHub Copilot** — geração de código e testes dentro do editor. Só entra a partir de Tasks/Implement, e só para Dev e Tech Lead.
- **Claude Cowork** — organização, tracking e checklists (papéis não-dev: DM, Product Specialist, QA).
- **Claude Design** — mockups de interface (Product Specialist, na etapa de Spec).
- **Azure DevOps** — board oficial de acompanhamento (todas as etapas, todos os papéis, mas quem escreve é DM/TL).
- **GitHub** — repositório e CI/CD (Implement → Deploy).

## 2. Mapa por papel e etapa

| Papel | Spec | Plan | Tasks | Implement | Review | Deploy |
|---|---|---|---|---|---|---|
| **Product Specialist** | Claude (chat) escreve `requirements.md`; Claude Design gera mockup | Claude (chat) esclarece dúvidas de escopo levantadas pelo TL | — | Claude (chat) responde dúvidas ad hoc de escopo | Claude (chat) valida se o comportamento entregue respeita guardrails/spec | Claude (chat) faz smoke check pós-deploy contra a spec |
| **Tech Lead** | Claude (chat) revisa viabilidade técnica do requirements.md | Claude (chat) escreve `plan.md` a partir do requirements.md + ADRs | Claude (chat) revisa/aprova `tasks.md` (Gate 2) | GitHub Copilot para gerar/testar trechos de referência; Claude (chat) para AGENTS.md e skills | GitHub (PR/code review) + Copilot como apoio; Claude (chat) para revisão de arquitetura (Gate 3) | GitHub Actions/CI; aprovação final de deploy (Gate 4) |
| **Desenvolvedor** | — | Claude (chat) para explorar abordagens técnicas | Claude (chat) converte `plan.md` em `tasks.md`; Copilot ajuda a quebrar em subtasks | GitHub Copilot (geração de código) + Claude (chat) para debugging/arquitetura, com MCP (filesystem/git/memory) | GitHub Copilot para ajustar após comentários; Claude (chat) para refatorar | GitHub (merge, dispara CI/CD) |
| **QA** | Claude (chat) avalia se verification criteria são testáveis | Claude (chat) inicia rascunho do `test-plan.md` a partir dos VCs | Claude (chat) finaliza cenários de teste; Claude Cowork organiza rastreabilidade teste→VC | Claude (chat) escreve/revisa skill de geração de testes | Claude (chat) + Claude Cowork validam cobertura e suficiência dos testes (Gate 4) | Claude Cowork confirma sign-off de testes antes do deploy |
| **Delivery Manager** | Claude Cowork cria item de spec no board; Claude (chat) apoia definição de processo | Claude Cowork atualiza status do board (Rascunho→Em Revisão); Azure DevOps | Azure DevOps cria work items a partir das tasks; Claude Cowork atualiza tracking (Gate 1/2) | Azure DevOps monitora progresso; Claude Cowork sinaliza bloqueios | Claude Cowork mantém checklist de validation gates (Gate 3) | Azure DevOps + Claude Cowork fecham o ciclo (status "Validada") |

## 3. Checkpoints humanos embutidos no fluxo

Os 4 gates abaixo são o esqueleto do processo, mas devem operar como checklists executáveis, não como validações genéricas.

1. **Gate 1 — Spec → Plan:** Product Specialist aprova o `requirements.md` antes do Tech Lead gerar o `plan.md`.
   - **Quem aprova:** Product Specialist.
   - **O que precisa estar presente:** requisitos claros, critérios de aceite verificáveis, escopo delimitado, guardrails explícitos.
   - **Critérios objetivos de aprovação:** não há ambiguidades críticas, todos os requisitos têm impacto e prioridade definidos, e a spec está pronta para virar plano.
   - **Prazo máximo:** até 24 horas úteis.
   - **Ação em caso de reprovação:** a spec retorna ao rascunho, com comentários explícitos e novo ciclo de revisão.

2. **Gate 2 — Tasks → Implement:** Tech Lead aprova o `tasks.md` antes do Dev iniciar a implementação.
   - **Quem aprova:** Tech Lead.
   - **O que precisa estar presente:** tasks atômicas, dependências claras, critérios de aceitação por tarefa, riscos e estimativas iniciais.
   - **Critérios objetivos de aprovação:** as tasks são executáveis por desenvolvedor, não dependem de interpretação ambígua e estão alinhadas ao plano.
   - **Prazo máximo:** até 24 horas úteis.
   - **Ação em caso de reprovação:** as tasks voltam para revisão, com replanejamento ou fragmentação adicional.

3. **Gate 3 — Code → Merge:** Tech Lead faz code review humano; PR precisa de 1 aprovação.
   - **Quem aprova:** Tech Lead.
   - **O que precisa estar presente:** diff revisado, testes relevantes, evidências de validação e resposta aos comentários.
   - **Critérios objetivos de aprovação:** não há problemas críticos de arquitetura, segurança, ou regressão; a mudança está consistente com a spec e o plano.
   - **Prazo máximo:** até 48 horas úteis.
   - **Ação em caso de reprovação:** PR retorna para ajuste, com issue de correção e nova rodada de revisão.

4. **Gate 4 — Tests → Deploy:** QA valida cobertura e cenários de teste; Tech Lead aprova o deploy.
   - **Quem aprova:** QA e Tech Lead.
   - **O que precisa estar presente:** cenários de teste cobrindo o fluxo principal e falhas principais, evidência de execução e status de abertura de riscos.
   - **Critérios objetivos de aprovação:** os testes cobrem os critérios de aceite, há evidência de execução e não há riscos críticos não mitigados.
   - **Prazo máximo:** até 24 horas úteis.
   - **Ação em caso de reprovação:** o deploy é bloqueado, e o time retorna para correção e revalidação.

### 3.1 Evidência mínima exigida para aprovação

Toda aprovação humana deve ser baseada em evidência, não em confiança implícita. O aprovador deve ter acesso a:

- artefato final revisado;
- lista objetiva de mudanças;
- justificativa da IA usada para gerar o rascunho;
- pontos pendentes ou riscos conhecidos;
- evidência de validação, quando aplicável.

### 3.2 Rascunho vs artefato aprovado

Qualquer saída gerada por IA entra no fluxo como **rascunho**. Ela só vira **aprovada** após:

- revisão humana;
- registro explícito da decisão;
- atualização do status no board ou no repositório.

### 3.3 Rollback e contingência

Se um artefato for reprovado ou se houver falha após deploy, o fluxo deve seguir uma contingência formal:

- voltar para a etapa anterior;
- abrir issue de correção;
- reexecutar validação do gate afetado;
- bloquear o deploy se o risco for crítico.

### 3.4 Regras de uso de IA por categoria de informação

O uso de IA deve seguir regras de segurança e responsabilidade:

- dados sensíveis, segredos, dados de cliente e documentos internos devem ter tratamento especial;
- não é permitido enviar dados sensíveis a ferramentas externas sem aprovação e sem redaction;
- decisões de negócio, arquitetura e risco não podem ser delegadas à IA sem validação humana.

### 3.5 Métricas de qualidade e custo

Para evoluir o processo com base em evidência, o time deve acompanhar, periodicamente:

- tempo médio de revisão por gate;
- taxa de retrabalho ou reprovação;
- número de artefatos reprovados;
- tempo de resposta do assistente;
- custo por ciclo ou por entrega.

## 4. Leitura do mapa

- **Copilot só aparece a partir de Tasks/Implement** — ele não participa da definição do que construir, só de como construir. Isso evita que decisões de escopo e arquitetura sejam geradas por um agente sem visão de negócio.
- **Cowork concentra-se em tracking e governança** — é a ferramenta de quem orquestra (DM, QA, PS), não de quem codifica.
- **Claude (chat) é transversal** — é o único agente presente em todas as etapas e todos os papéis, o que o torna o principal ponto de padronização (via AGENTS.md e skills).
- **Cada papel usa IA para acelerar seu próprio artefato, nunca para aprovar o artefato de outro papel** — quem aprova é sempre humano, e é sempre o dono natural da etapa seguinte (PS aprova para o TL, TL aprova para o Dev, TL aprova para o Deploy).

## 5. Fluxo de exceção

O fluxo de exceção opera em paralelo ao fluxo principal de trabalho. Ele é acionado somente quando uma etapa do ciclo Spec → Plan → Tasks → Implement → Review → Deploy for bloqueada por urgência, risco, falha ou necessidade de decisão imediata.

### 5.1 Como ele se encaixa no fluxo normal

O fluxo normal continua sendo:

Spec → Plan → Tasks → Implement → Review → Deploy

O fluxo de exceção não substitui esse percurso; ele cria uma trilha de contingência que pode ser iniciada em qualquer ponto do ciclo. Em outras palavras, o trabalho segue a trilha principal, mas, se algo sair do esperado, entra em uma rota paralela de governança.

### 5.2 Quando o fluxo de exceção é acionado

A exceção deve ser usada quando ocorrer um dos cenários abaixo:

- prazo crítico de entrega;
- bloqueio de dependência;
- erro grave detectado em artefato gerado por IA;
- mudança de escopo urgente;
- risco de segurança, compliance ou impacto em cliente.

### 5.3 Passos do fluxo de exceção

1. **Acionar a exceção** — a equipe identifica o problema e registra que a etapa está fora do fluxo normal.
2. **Registrar contexto** — documentar motivo, impacto, artefato afetado, responsável pela decisão e prazo para normalização.
3. **Aprovar a exceção** — a decisão é tomada por um responsável adequado ao nível de impacto:
   - **Baixo**: Tech Lead;
   - **Médio**: Tech Lead + Product Specialist ou QA;
   - **Alto**: Delivery Manager + Tech Lead + Product Specialist.
4. **Aplicar controles temporários** — revisão humana adicional, validação explícita, evidência mínima e limites claros de prazo.
5. **Retornar ao fluxo normal** — o trabalho volta para a mesma etapa anterior, ou é reprocessado por rollback/correção, conforme o caso.

### 5.4 Regra de ouro

Exceção não significa “pular validação”. Significa “validar com mais rigor, de forma explícita e com responsabilidade definida”.

