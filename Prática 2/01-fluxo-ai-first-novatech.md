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

1. **Gate 1 — Spec → Plan:** Product Specialist aprova o `requirements.md` antes do Tech Lead gerar o `plan.md`.
2. **Gate 2 — Tasks → Implement:** Tech Lead aprova o `tasks.md` antes do Dev iniciar a implementação.
3. **Gate 3 — Code → Merge:** Tech Lead faz code review humano; PR precisa de 1 aprovação.
4. **Gate 4 — Tests → Deploy:** QA valida cobertura e cenários de teste; Tech Lead aprova o deploy.

Esses 4 gates são o esqueleto do checklist detalhado (quem aprova, o que verifica, prazo, o que acontece se reprovar), a ser formalizado como template no Cowork.

## 4. Leitura do mapa

- **Copilot só aparece a partir de Tasks/Implement** — ele não participa da definição do que construir, só de como construir. Isso evita que decisões de escopo e arquitetura sejam geradas por um agente sem visão de negócio.
- **Cowork concentra-se em tracking e governança** — é a ferramenta de quem orquestra (DM, QA, PS), não de quem codifica.
- **Claude (chat) é transversal** — é o único agente presente em todas as etapas e todos os papéis, o que o torna o principal ponto de padronização (via AGENTS.md e skills).
- **Cada papel usa IA para acelerar seu próprio artefato, nunca para aprovar o artefato de outro papel** — quem aprova é sempre humano, e é sempre o dono natural da etapa seguinte (PS aprova para o TL, TL aprova para o Dev, TL aprova para o Deploy).
