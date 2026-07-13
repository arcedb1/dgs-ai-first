# CHANGE-MANAGEMENT.md — Gestão de Mudança em Specs Já em Implementação

> Complementa `02-GOVERNANCE.md`. Aquele documento rege a criação e aprovação inicial de `requirements.md` / `plan.md` / `tasks.md`. Este documento rege o que acontece quando uma dessas specs **já foi aprovada, o time já começou a implementar, e surge a necessidade de mudá-la** — novo requisito, decisão técnica revista, cenário de falha achado pelo QA, contradição documental, pedido de negócio de última hora etc.

**Princípio obrigatório: specs são artefatos vivos.** Mudar uma spec em implementação é normal e esperado, não uma falha de planejamento. O que precisa ser controlado é **como** se muda — quem propõe, quem aprova, o que acontece com o trabalho em andamento, e como o rastro fica auditável — nunca **se** se muda. Bloquear mudança para "proteger o plano" é o antipadrão que este processo existe para evitar; permitir mudança sem controle, gerando código órfão e retrabalho invisível, é o outro extremo que ele também evita.

---

## 1. Quem pode propor uma mudança

Qualquer papel do time pode **propor**. Ninguém precisa de autoridade de aprovação para levantar a mão — o funil de decisão é o que filtra, não a permissão de falar:

| Papel | Gatilho típico de proposta |
|---|---|
| Product Specialist | Negócio pediu novo critério, prioridade mudou, escopo cresceu |
| Tech Lead | Decisão de arquitetura revista, ADR obsoleto, integração inviável como planejada |
| Dev | Ambiguidade encontrada durante a codificação, task não bate com o plan |
| QA | Cenário de falha não coberto, critério de aceite não testável na prática |
| Delivery Manager | Contradição documental entre módulos, risco de prazo/rastreabilidade |

Toda proposta é registrada como um **Change Request (CR)** — um item no board (Azure DevOps/Cowork) linkado à spec afetada, com: origem, descrição do gap, módulo/artefato impactado, urgência percebida. Sem CR registrado, não há mudança de spec em implementação — mesmo uma "correção rápida" no arquivo.

---

## 2. Quem aprova, por tipo de artefato afetado

A regra de `02-GOVERNANCE.md` §1 continua valendo: **quem aprova é sempre o dono natural do artefato**, nunca quem só vai consumi-lo. Isso não muda porque a implementação já começou.

| Artefato afetado | Aprovador da mudança | Por quê |
|---|---|---|
| `requirements.md` (o QUÊ) | **Product Specialist** | Só quem tem visão de negócio decide se o escopo/outcome realmente mudou |
| `plan.md` (o COMO) | **Tech Lead** | Só quem tem autoridade de arquitetura decide se a decisão técnica deve ser revista |
| `tasks.md` (decomposição) | **Tech Lead** | Mesma regra do Gate 2: só o dono do `plan.md` confirma que a nova decomposição ainda cobre 100% do plano |

Se a mudança se origina em requirements, o Tech Lead **não** aprova sozinho uma alteração de plan "de passagem" — ele reavalia formalmente (§5), mesmo que a alteração pareça pequena.

---

## 3. Classificação de impacto

Toda CR é classificada por quem a tria (Tech Lead para mudanças técnicas, Product Specialist para mudanças de escopo) em um dos três níveis abaixo, antes de qualquer aprovação:

| Nível | Critério | O que dispara |
|---|---|---|
| **Menor** | Não altera critério de aceite, contrato de API, ou decisão de arquitetura já implementada. Ex.: clarificação de texto, ajuste de mensagem de erro, task renomeada sem mudar escopo. | Ajuste direto no arquivo + commit de status; **não** reabre gate; registrado no changelog da spec (§6). Notificação assíncrona ao dono do artefato. |
| **Significativa** | Altera um critério de aceite, adiciona/remove um cenário, ou muda uma decisão técnica sem quebrar contrato externo já publicado. Ex.: novo cenário de falha, novo campo opcional, troca de biblioteca interna. | Reabre o Gate correspondente (Gate 1 se requirements/plan, Gate 2 se tasks). Spec volta a `rascunho` → `em-revisao` → `aprovado`. Tasks em andamento avaliadas conforme §4. |
| **Crítica** | Quebra contrato já implementado/publicado (API pública, schema de dados, SLA contratual), ou exige retrabalho de módulo(s) já mesclado(s) em `main`. Ex.: mudança de política de negócio que invalida uma feature já em produção. | Reabre Gate 1 **e** exige alinhamento explícito do Delivery Manager (risco de prazo/rastreabilidade cross-módulo) antes de qualquer novo trabalho. Pode gerar um novo ADR obrigatório em `docs/adr/`. |

A classificação em si é registrada no CR — não é opcional nem informal ("achei que era pequeno" não é um critério; os critérios objetivos da tabela são).

### 3.1 Segregação entre proponente e triador

Quando a mesma pessoa propõe a CR (§1) e seria naturalmente quem a classifica (§3) — o caso mais comum é o Tech Lead propondo e triando uma mudança técnica — **a classificação exige um segundo revisor** antes de ser aceita como final:

- CR técnica proposta pelo Tech Lead → Dev Sênior do módulo confirma a classificação.
- CR de escopo proposta pelo Product Specialist → Tech Lead confirma a classificação (viabilidade) sem poder rebaixá-la sozinho de Significativa/Crítica para Menor.
- Se o segundo revisor discordar do nível proposto, prevalece o nível **mais alto** entre os dois até o Delivery Manager decidir (desempate), nunca o mais baixo por padrão.

Isso existe porque quem propõe e classifica ao mesmo tempo tem incentivo natural — sob pressão de prazo, não por má-fé — de subclassificar como Menor para evitar reabrir o gate. A mesma regra de "quem cria não aprova sozinho" de `02-GOVERNANCE.md §1` se aplica aqui à classificação, não só à aprovação final.

### 3.2 Auditoria periódica de classificações "Menor"

Mensalmente, o Delivery Manager revisa a lista de CRs classificadas como Menor no período, por módulo. Não é uma reabertura individual de cada CR — é uma checagem de padrão:

- Se um módulo concentra uma proporção desproporcional de CRs "Menor" frente aos demais, ou se uma sequência de CRs "Menor" no mesmo artefato, somadas, equivalem a uma mudança Significativa não reconhecida como tal, o Delivery Manager abre uma CR de auditoria própria, classificada como Significativa, para forçar a spec a passar pelo gate que as mudanças acumuladas deveriam ter disparado individualmente.
- Este é um sinal para investigar, não uma prova de má classificação — a auditoria existe para pegar erosão sistemática de critério, não para punir triagens pontuais.

---

## 4. Efeito em tasks já em andamento

Quando uma CR é aceita, toda task em `tasks.md` referenciando o artefato mudado é avaliada individualmente pelo Tech Lead (nunca a spec inteira é congelada por atacado):

1. **Task não iniciada** → marcada `bloqueada-por-CR-<id>` no `tasks.md`, não inicia até o gate afetado ser reaprovado.
2. **Task em andamento, código ainda não bate com a mudança** → **pausa**. O dev não continua codando contra uma spec que já se sabe desatualizada — isso é exatamente o que gera código órfão. Work-in-progress é commitado em branch (não descartado) com marcação `WIP (pausado por CR-<id>)`.
3. **Task em andamento, código já compatível com a mudança** (ex.: o dev já tinha implementado de um jeito que cobre o novo cenário) → segue, mas a task é re-linkada explicitamente à nova versão do `plan.md`/`requirements.md` antes de PR, para não perder rastreabilidade.
4. **Task já mesclada em `main`** → não é revertida automaticamente. Vira uma nova task de ajuste, cotada e priorizada como qualquer outra, referenciando a CR que a originou.

Regra de ouro desta seção: **nenhuma task continua sendo codada contra uma spec em status diferente de `aprovado`.** Isso é a mesma regra de `02-GOVERNANCE.md §5.1`, agora aplicada explicitamente ao meio da implementação, não só à criação inicial.

### 4.1 Mecanismo de verificação (a regra de ouro não é só acordo de cavalheiros)

Sem este projeto ter CI configurado para bloquear automaticamente, a regra acima depende de disciplina — o que, sob pressão de prazo, é exatamente o ponto em que ela tende a ser ignorada ("é rápido, já sei o que fazer, termino mesmo assim"). Para reduzir isso a algo verificável, e não só normativo:

- Todo `docs/pull-requests/PR-NNNN.md` (Gate 3) ganha um campo obrigatório: **"Status da spec-fonte no momento do commit"** — o autor da task preenche com o status (`aprovado`/`rascunho`/`em-revisao`) de cada `requirements.md`/`plan.md` referenciado pela task, lido diretamente do cabeçalho do arquivo.
- O Tech Lead, ao revisar o PR (Gate 3), rejeita sumariamente qualquer PR cujo campo indique um status diferente de `aprovado` — sem julgamento de mérito do código, é rejeição automática por processo.
- Isso não impede tecnicamente o commit (não há hook de CI), mas move a verificação de "confiar que o dev pausou" para "checar um campo declarado e auditável no PR", que fica registrado permanentemente — se o campo mentir, isso também é auditável depois via `git log --follow` no arquivo de spec vs. data do commit.

---

## 5. Propagação em cascata

Mudança em `requirements.md` não fica isolada — o Tech Lead é obrigado a reavaliar `plan.md`, mesmo que a mudança pareça não tocar arquitetura:

```
requirements.md muda (Product Specialist marca `rascunho`, CR aberto)
        │
        ▼
Tech Lead reavalia plan.md vigente
        │
   ainda coerente? ──── SIM ──→ plan.md permanece `aprovado`,
        │                        anotação no changelog "revisado, sem mudança" (CR-<id>)
        NÃO
        │
        ▼
plan.md volta para `rascunho`, reescrito a partir do novo requirements.md
        │
        ▼
tasks.md: tasks referenciando as seções alteradas do plan são identificadas
por referência cruzada e marcadas `bloqueada-por-CR-<id>`
        │
        ▼
Gate 1 reexecutado (requirements + plan) → Gate 2 reexecutado (tasks)
        │
        ▼
Só então: novo código pode ser gerado a partir da spec atualizada
```

Não existe atalho em que `plan.md` é editado "só um pouco" sem religar ao requirement que motivou — isso é proibido mesmo sob pressão de prazo (mesma regra de `02-GOVERNANCE.md §5.1`).

---

## 6. Registro e rastreabilidade

Toda spec ganha uma seção de changelog no próprio arquivo (abaixo do cabeçalho de status já definido em `02-GOVERNANCE.md §2.2`):

```markdown
## Changelog
| Data | CR | Impacto | Descrição | Aprovado por |
|---|---|---|---|---|
| 2026-07-12 | CR-014 | Significativa | Novo cenário: feedback duplicado no mesmo ticket | Tech Lead (fulano) |
```

- O commit que altera o conteúdo da spec referencia o CR na mensagem: `spec(feedback-api): requirements → rascunho (CR-014: cenário de feedback duplicado)`.
- O commit de mudança de status segue o padrão já definido: `spec(<modulo>): <artefato> → <novo-status>` — mudança de status e mudança de conteúdo continuam em commits separados (`02-GOVERNANCE.md §2.3`).
- Toda task nova ou reaberta por causa de uma CR cita o `CR-<id>` na descrição, além do link ao `plan.md` de origem.
- Nunca reescrever histórico (`--amend`, `rebase -i`) para "esconder" uma volta de status — o rastro da mudança é o próprio valor de auditoria do processo.

---

## 7. Gatilho de atualização do board

| Evento | Status anterior no board | Novo status no board |
|---|---|---|
| CR aberto, ainda não triado | "Em Implementação" | "Em Implementação" + tag `CR-<id> pendente` (sem mudar coluna ainda) |
| CR classificado como Menor, ajuste direto | "Em Implementação" | Sem mudança de coluna; changelog atualizado |
| CR classificado como Significativa ou Crítica | "Em Implementação" | Volta para **"Em Revisão"** (mesma coluna do Gate 1/2 original) |
| Gate correspondente reaprovado | "Em Revisão" | Volta para **"Em Implementação"** |
| Task mesclada mesmo após CR crítica gerar ajuste | "Concluído" | Reaberto como nova task filha, linkada à CR — o item original não é reaberto/reeditado |

O board nunca deve mostrar "Em Implementação" para uma spec cujo `requirements.md` ou `plan.md` está em `rascunho`/`em-revisao` no arquivo — os dois precisam estar sincronizados; se um dev perceber divergência, é motivo suficiente para abrir uma CR de correção do próprio processo.

---

## 8. Exemplo aplicado — QA encontra cenário de falha na API de feedback

**Contexto:** `specs/feedback-api/` está `aprovado` em todos os três artefatos, board em "Em Implementação", dev já codificou as tasks 1 a 3 de `tasks.md` (validação de payload, persistência, retorno de sucesso). QA, testando manualmente, descobre que **enviar feedback duplicado para o mesmo ticket dentro de 5 minutos não é tratado** — a API aceita e cria dois registros, e não há critério de aceite em `requirements.md` cobrindo esse caso.

1. **Proposta (§1):** QA abre CR-014 no board, linkado a `specs/feedback-api/`, descrevendo o gap e anexando o passo a passo de reprodução.
2. **Triagem/classificação (§3):** Product Specialist avalia — isso é uma regra de negócio nova (o que fazer com duplicidade: rejeitar? mesclar? avisar o usuário?), não um bug de código. Classificado como **Significativa**: adiciona um cenário e um critério de aceite, mas não quebra contrato de API já publicado (a API ainda não foi liberada externamente).
3. **Aprovação de requirements (§2):** Product Specialist decide a regra de negócio ("rejeitar duplicidade e retornar 409 com mensagem ao usuário"), edita `requirements.md`, marca `rascunho`, abre commit `spec(feedback-api): requirements → rascunho (CR-014: cenário de feedback duplicado)`.
4. **Propagação (§5):** Tech Lead reavalia `plan.md` — a regra exige uma checagem de duplicidade antes da persistência, que não estava no plano original. `plan.md` também volta a `rascunho` e ganha a decisão técnica (índice único por `ticket_id + janela de 5 min`, ou consulta prévia — Tech Lead decide e documenta, referenciando ADR se for decisão não trivial).
5. **Efeito em tasks (§4):**
   - Task 1 (validação de payload) — já mesclada em `main` → não revertida; vira base para uma **task nova** "3.1 — validar duplicidade de feedback (CR-014)".
   - Task 2 (persistência) — em andamento, código ainda não trata duplicidade → **pausada**, branch commitada como WIP, dev não continua até o plan ser reaprovado.
   - Task 3 (retorno de sucesso) — não iniciada → marcada `bloqueada-por-CR-014`.
6. **Gates reexecutados:** Gate 1 (requirements + plan) roda de novo com Product Specialist e Tech Lead. Aprovado → `tasks.md` é atualizado (nova task 3.1, tasks 2 e 3 desbloqueadas com referência à seção atualizada do plan) → Gate 2 roda com Tech Lead aprovando a nova decomposição.
7. **Registro (§6):** changelog de `requirements.md` e `plan.md` ganham a linha do CR-014; commits de conteúdo e de status separados; `docs/pull-requests/` da eventual PR que resolve a task 3.1 referencia `CR-014` e `specs/feedback-api/tasks.md#task-3.1`.
8. **Board (§7):** `feedback-api` volta de "Em Implementação" para "Em Revisão" no passo 3, retorna para "Em Implementação" assim que o Gate 1 é reaprovado no passo 6.

Resultado: o cenário de falha vira parte permanente da spec (não um patch informal no código), o trabalho já feito não é jogado fora nem seguido cegamente, e qualquer pessoa lendo `specs/feedback-api/` seis meses depois vê exatamente por que a regra de duplicidade existe — via changelog, ADR e CR-014.
