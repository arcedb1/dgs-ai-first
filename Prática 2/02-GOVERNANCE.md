# GOVERNANCE.md — Governança de Specs (SDD) do NovaTech Assistant

> Este documento rege como `requirements.md`, `plan.md` e `tasks.md` são criados, revisados, aprovados, nomeados, versionados e rastreados nos 5 módulos iniciais do projeto: pipeline de ingestão, API de busca, API de feedback, bot do Teams e painel web.

**Princípio central: specs são artefatos vivos.** Nenhum dos três arquivos é escrito uma vez e congelado. Eles evoluem junto com o código, o domínio e as decisões do time — e cada evolução relevante deixa rastro em Git (commit/PR) e no board (Azure DevOps/Cowork). Um `requirements.md` "aprovado" pode voltar a rascunho se o escopo mudar; um `plan.md` pode ganhar uma nova versão se uma decisão de arquitetura for revertida. Tratar specs como imutáveis é o erro que este processo existe para evitar.

---

## 1. Responsabilidades por artefato

| Artefato | Cria | Revisa | Aprova | Papel do artefato |
|---|---|---|---|---|
| `requirements.md` | Product Specialist (com apoio de Claude chat) | Tech Lead (viabilidade técnica) | **Product Specialist** | Define o QUE e o PORQUÊ — outcomes de negócio, escopo, critérios de aceite testáveis |
| `plan.md` | Tech Lead (com apoio de Claude chat) | Product Specialist + Dev Sênior | **Tech Lead** | Define o COMO — arquitetura, decisões técnicas, ADRs referenciados |
| `tasks.md` | Dev (com apoio de GitHub Copilot/Claude) | Tech Lead | **Tech Lead** | Decompõe o plano em unidades atômicas executáveis por agentes de IA |

### Por que esta atribuição é coerente

- **`requirements.md` → Product Specialist cria e aprova.** É quem tem visão de negócio e linguagem do usuário; é o único papel com autoridade para dizer "isto é o que o negócio precisa". O Tech Lead revisa para vetar requisitos tecnicamente inviáveis antes que virem plano, mas não pode aprovar em nome do negócio — isso violaria a regra de que "quem aprova é sempre o dono natural da etapa", nunca quem vai consumir o artefato a seguir.
- **`plan.md` → Tech Lead cria e aprova.** É a única pessoa com autoridade e contexto de arquitetura para decidir como o sistema será construído (stack, integrações, ADRs). O Product Specialist revisa para garantir que o plano não reduz silenciosamente o escopo de negócio; o Dev Sênior revisa por viabilidade de implementação — mas a aprovação final é técnica, então fica com o Tech Lead.
- **`tasks.md` → Dev cria (com Copilot), Tech Lead aprova.** Copilot só entra a partir de Tasks/Implement porque decompor um plano em unidades atômicas é um problema de execução, não de escopo ou arquitetura — não requer visão de negócio nem autoridade de decisão técnica de alto nível. Quem melhor sabe se uma task é "atômica o suficiente para ser codada sem ambiguidade" é quem vai codá-la. A aprovação fica com o Tech Lead porque ele é o dono do `plan.md` do qual as tasks derivam — só ele pode confirmar que a decomposição cobre 100% do plano sem distorcer decisões de arquitetura.

Este desenho espelha o RACI já em uso no board (Anexo 01-fluxo-ai-first): cada papel usa IA para acelerar seu **próprio** artefato, nunca para aprovar o artefato de outro papel.

### RACI consolidado

| Atividade | Product Specialist | Tech Lead | Dev | QA | Delivery Manager |
|---|---|---|---|---|---|
| Escrever `requirements.md` | **R/A** | C | I | C | I |
| Escrever `plan.md` | C | **R/A** | C | I | I |
| Escrever `tasks.md` | I | A | **R** | I | I |
| Definir critérios de aceite testáveis | R | C | I | **C/A** | I |
| Aprovar Gate 1 (Spec→Plan) | **A** | R | – | – | I |
| Aprovar Gate 2 (Tasks→Implement) | I | **A** | R | – | I |
| Garantir rastreabilidade spec↔código↔teste | I | C | C | C | **A** |

*R = Responsável pela execução, A = Aprova/presta contas, C = Consultado, I = Informado.*

---

## 2. Nomenclatura e versionamento

### 2.1 Pastas e arquivos

| Elemento | Convenção | Exemplo |
|---|---|---|
| Pasta do módulo | slug em `kebab-case`, curto, sem prefixo redundante | `pipeline-ingestao`, `query-endpoint`, `feedback-api`, `teams-bot`, `painel-web` |
| Requirements | sempre `requirements.md` | `specs/query-endpoint/requirements.md` |
| Plan | sempre `plan.md` | `specs/query-endpoint/plan.md` |
| Tasks | sempre `tasks.md` | `specs/query-endpoint/tasks.md` |
| ADR referenciado por uma spec | `docs/adr/NNNN-titulo-da-decisao.md` | `docs/adr/0001-escolha-azure-openai.md` |
| Test plan (QA, gerado a partir dos VCs) | `test-plan.md` na mesma pasta do módulo | `specs/feedback-api/test-plan.md` |

Não versionar specs por número de arquivo (`requirements-v2.md`). O nome do arquivo é fixo; a versão vive no **histórico do Git** e em um cabeçalho de status dentro do próprio arquivo.

### 2.2 Esquema de status (não semântico)

Como specs mudam de mãos (rascunho → revisão → aprovado) mais do que ganham "versões" no sentido de release, o versionamento é **por status**, não semântico (`v1.2.0`). Todo `requirements.md`, `plan.md` e `tasks.md` deve abrir com um cabeçalho:

```markdown
---
status: rascunho | em-revisao | aprovado | revisao-solicitada
aprovado_por: <nome ou "—">
data_aprovacao: <YYYY-MM-DD ou "—">
versao_historico: ver `git log --follow <arquivo>`
---
```

- **rascunho** — recém-criado ou recém-alterado por IA, ainda não revisado por humano.
- **em-revisao** — no board, aguardando decisão do gate correspondente.
- **aprovado** — passou no gate; é a versão vigente que autoriza a próxima etapa.
- **revisao-solicitada** — reprovado; comentários registrados no PR ou inline no arquivo, aguardando novo ciclo.

Uma spec `aprovado` pode voltar para `rascunho` a qualquer momento do projeto (mudança de escopo, bug de produção, novo requisito) — isso é esperado, não uma exceção. Quando isso acontece, o Gate correspondente é reexecutado.

### 2.3 Convivência com o histórico do Git

- O status vive no arquivo (fonte da verdade "estado atual"); o histórico de *como* se chegou lá vive no Git (`git log`, `git blame`, diffs de PR).
- Toda mudança de status é um commit dedicado (não misturado com edição de conteúdo), com mensagem no padrão:
  `spec(<modulo>): <requirements|plan|tasks> → <novo-status>`
  Exemplo: `spec(query-endpoint): requirements → aprovado`
- Mudanças de conteúdo pós-aprovação (spec viva) exigem um novo ciclo do gate afetado e um commit separado documentando o motivo no corpo da mensagem.
- Nunca reescrever o histórico de uma spec (`--amend`, `rebase -i`) — o rastro de quem mudou o quê e quando é parte da governança, não um artefato descartável.

---

## 3. Localização no repositório

Specs vivem versionadas junto ao código, uma pasta por módulo, sob `/specs/`, seguindo a estrutura já adotada no repositório (Anexo C):

```
db1/novatech-assistant/
├── AGENTS.md
├── docs/
│   ├── adr/
│   │   ├── template.md
│   │   └── 0001-escolha-azure-openai.md
│   ├── pull-requests/
│   │   └── PR-NNNN.md              # checklist do Gate 3 preenchido
│   └── runbooks/
│
├── specs/
│   ├── pipeline-ingestao/
│   │   ├── requirements.md         # Product Specialist
│   │   ├── plan.md                 # Tech Lead
│   │   └── tasks.md                # Dev + Copilot
│   ├── query-endpoint/
│   │   ├── requirements.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── test-plan.md            # QA, a partir dos verification criteria
│   ├── feedback-api/
│   │   ├── requirements.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── teams-bot/
│   │   ├── requirements.md
│   │   ├── plan.md
│   │   └── tasks.md
│   └── painel-web/
│       ├── requirements.md
│       ├── plan.md
│       └── tasks.md
│
├── src/
│   ├── functions/query/ ...        # código que implementa specs/query-endpoint/
│   ├── functions/feedback/ ...      # código que implementa specs/feedback-api/
│   ├── pipeline/ ...                # código que implementa specs/pipeline-ingestao/
│   ├── bot/ ...                     # código que implementa specs/teams-bot/
│   └── web/ ...                     # código que implementa specs/painel-web/
│
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/
```

Regra de localização: **1 módulo = 1 pasta em `/specs/`, com nome idêntico ao usado nas pastas de código correspondentes sempre que possível** (`query-endpoint` ↔ `src/functions/query/`), para que a relação spec↔código seja óbvia por convenção de nome, sem precisar de um índice separado.

---

## 4. Checkpoints humanos

Cada transição é um dos 4 gates já em uso no projeto (ver `01-checklist-validation-gates.md`), reafirmados aqui na ótica de specs:

| Transição | O que é validado | Quem assina | Onde é registrado |
|---|---|---|---|
| **Gate 1 — `requirements.md` → `plan.md`** | Outcomes de negócio claros, escopo delimitado, critérios de aceite testáveis, sem ambiguidade de domínio | Product Specialist | Status no cabeçalho do arquivo (`aprovado`) + item do board (Azure DevOps/Cowork) movido para "Aprovado" + commit de status |
| **Gate 2 — `tasks.md` → Implement** | Tasks atômicas, dependências mapeadas, cobertura de 100% do `plan.md`, critérios de aceite por task | Tech Lead | Comentário task a task no `tasks.md` (se reprovado parcialmente) + status no cabeçalho + board |
| *(referência) Gate 3 — Code → Merge* | Diff revisado, testes passando, aderência ao AGENTS.md/skills | Tech Lead (PR, 1 approval) | `docs/pull-requests/PR-NNNN.md` + PR no Git |
| *(referência) Gate 4 — Tests → Deploy* | Cobertura ≥80%, todo verification criterion com teste correspondente | QA + Tech Lead | Sign-off no board (Cowork) |

Regras que se aplicam a **todos** os gates:

- Todo artefato gerado por IA entra como **rascunho**. Só vira **aprovado** após revisão humana explícita — nunca por decurso de prazo ou ausência de objeção.
- O aprovador precisa ter acesso a: artefato final, lista objetiva de mudanças, justificativa da IA que gerou o rascunho, riscos/pendências conhecidos.
- Reprovação não é bloqueio silencioso: gera comentário explícito (inline no arquivo ou no PR), volta o item para o status anterior no board, e abre novo ciclo com prazo definido (24h para Gates 1 e 2, conforme checklist vigente).
- Gate 2 permite aprovação parcial: tasks já aprovadas dentro do mesmo `tasks.md` seguem para implementação sem esperar o ajuste das reprovadas.

### 4.1 Backup de aprovador (Tech Lead indisponível)

O Tech Lead é o único aprovador dos Gates 2, 3 e parte do 4 — um ponto único de falha se estiver de férias, desligado ou sobrecarregado. Quando isso acontece:

- O Dev Sênior mais experiente do módulo assume a aprovação como **substituto temporário**, seguindo o fluxo de exceção já definido (impacto **Baixo**, conforme seção 5.3 do fluxo AI First).
- A substituição é registrada explicitamente no campo `aprovado_por` do cabeçalho da spec, com a nota `(substituto por indisponibilidade do TL)`.
- O Tech Lead titular revisa as aprovações feitas em sua ausência assim que retornar; qualquer discordância reabre o gate correspondente.

---

## 5. Rastreabilidade

### 5.1 Propagação de uma mudança em requirements até tasks

1. Mudança em `requirements.md` (nova regra de negócio, requisito removido, critério de aceite alterado) → o Product Specialist marca o arquivo como `rascunho` novamente e abre um commit `spec(<modulo>): requirements → rascunho (motivo: ...)`.
2. O Tech Lead reavalia se o `plan.md` vigente ainda é coerente. Se não for, `plan.md` também volta para `rascunho` e é reescrito a partir do novo `requirements.md` — **nunca editado silenciosamente sem religar ao requirement que motivou a mudança**.
3. Tasks afetadas em `tasks.md` são identificadas por referência cruzada (toda task deve citar o ID/seção do `plan.md` de onde deriva) e marcadas para revisão; tasks não afetadas continuam válidas.
4. Cada arquivo alterado passa novamente pelo gate correspondente (Gate 1 para requirements/plan, Gate 2 para tasks) antes de qualquer novo código ser gerado a partir dele.

Regra prática: **nenhuma task pode ser implementada se o `plan.md` ou `requirements.md` do qual deriva estiver em status diferente de `aprovado`.** Isso é o que impede que specs vivas gerem código a partir de uma base já obsoleta.

### 5.2 Rastro spec ↔ código ↔ testes

- **Task → commit/PR:** toda branch e PR referenciam o módulo e a task, ex.: `feat(query-endpoint): implementa task 3.2 - validação de input`. O `docs/pull-requests/PR-NNNN.md` linka explicitamente para `specs/query-endpoint/tasks.md#task-3.2`.
- **Verification criterion → teste:** cada verification criterion em `requirements.md` deve ter pelo menos um teste correspondente em `tests/`, e o `test-plan.md` do módulo (quando existir) documenta esse mapeamento criterion → caso de teste. Este é justamente o critério objetivo do Gate 4.
- **Decisão de arquitetura → ADR → plan:** toda decisão técnica não trivial referenciada em `plan.md` deve existir como ADR em `docs/adr/`; o Gate 1 já exige que toda "prior decision" citada em `requirements.md` tenha ADR correspondente.
- **Ferramenta de rastreabilidade organizacional:** Claude Cowork mantém o rastro teste→verification-criterion e o status geral no board; o Git mantém o rastro spec→código via mensagens de commit e PRs linkados. Nenhuma rastreabilidade crítica deve depender só de memória do time — precisa estar em um desses dois lugares.

---

## 6. Regra de ouro

Uma spec aprovada não é um contrato imutável — é o estado mais recente de um entendimento compartilhado, sujeito a revisão sempre que a realidade do negócio, da arquitetura ou da implementação mudar. O que é imutável é o **processo**: toda mudança relevante passa pelo gate certo, é aprovada pelo dono certo, e deixa rastro em Git e no board. Pular isso sob pressão de prazo é o que este documento existe para impedir.
