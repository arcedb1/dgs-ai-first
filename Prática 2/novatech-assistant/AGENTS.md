# AGENTS.md — NovaTech Assistant

> Constitution do projeto. Todo agente de IA (Copilot, Claude Code) lê este arquivo antes de gerar qualquer artefato.
> As seções abaixo são preenchidas por papéis diferentes nos exercícios do Cenário 2.

## Project Overview
<!-- TODO (Tech Lead — Ex. 2.1) -->

## Tech Stack & Architecture
<!-- TODO (Tech Lead — Ex. 2.1): inclui regras de gerenciamento de contexto da ADR-0002 -->

## Coding Standards (Tech Lead)
<!-- TODO (Tech Lead — Ex. 2.1) -->

## Product Rules & Guardrails (Product Specialist)
<!-- TODO (Product Specialist — Ex. 2.3) -->

## Testing Standards (QA)
<!-- TODO (QA — Ex. 2.1) -->

## Project Management Rules (Delivery Manager)

Esta seção é normativa para qualquer agente de IA que gere tasks, issues, ADRs ou artefatos de gestão do projeto. Regras aqui têm precedência sobre convenções genéricas de mercado. Em caso de conflito com outra seção deste arquivo, esta seção governa nomenclatura, rastreabilidade e fluxo de aprovação.

### 1. Nomenclatura de Tasks e Issues

**Formato do título (obrigatório):**

```
[<módulo>] <Verbo imperativo> <objeto> (spec: <spec-slug>)
```

- `<módulo>` DEVE ser um dos valores: `ingestao`, `api-assistente`, `bot-teams`, `painel-web`, `infra`, `cross-cutting`.
- `<Verbo imperativo>` em português, no infinitivo ou imperativo (ex.: "Implementar", "Corrigir", "Adicionar", "Remover", "Investigar"). NUNCA usar gerúndio ("Implementando") ou substantivo solto ("Implementação de X").
- `<spec-slug>` referencia o diretório da spec de origem em `/specs/<modulo>/`.
- Exemplos válidos:
  - `[api-assistente] Implementar filtro de contradições pendentes (spec: filtro-contradicoes)`
  - `[bot-teams] Corrigir timeout em respostas longas (spec: bot-resposta-longa)`
- Exemplo inválido: `Ajustes no bot` (sem módulo, sem verbo imperativo, sem referência de spec).

**Labels obrigatórias:**

| Label | Valores permitidos | Obrigatória? |
|---|---|---|
| `modulo` | `ingestao`, `api-assistente`, `bot-teams`, `painel-web`, `infra`, `cross-cutting` | Sim |
| `tipo` | `feature`, `bug`, `debt`, `spike`, `doc` | Sim |
| `gate-atual` | `gate-1-spec-plan`, `gate-2-tasks-implement`, `gate-3-code-merge`, `gate-4-tests-deploy`, `concluido` | Sim |
| `prioridade` | `p0-critica`, `p1-alta`, `p2-media`, `p3-baixa` | Sim |
| `compliance-pendente` | `true` | Só quando a task tocar um dos 12 documentos com contradição pendente de Compliance |

Regra: um agente NUNCA cria uma task sem as 4 labels obrigatórias preenchidas. Se o valor correto não puder ser inferido, o agente deve perguntar antes de criar a task, não usar um valor padrão arbitrário.

**Rastreabilidade (obrigatória em toda task/issue):**

Todo corpo de task DEVE conter, como primeiras linhas, o bloco:

```
Spec de origem: /specs/<modulo>/<spec-slug>/requirements.md
Plan de origem: /specs/<modulo>/<spec-slug>/plan.md
ADR relacionado: /docs/adr/ADR-NNNN-<slug>.md  (ou "Nenhum" se não aplicável)
```

Se a task não referenciar uma spec existente em `/specs/<modulo>/`, o agente DEVE recusar-se a criá-la e sinalizar que falta a etapa de Spec Driven Development (requirements.md → plan.md → tasks.md).

### 2. Documentação de Decisões (ADRs)

- Regra geral: toda decisão técnica ou de escopo que altere arquitetura, contrato de API, modelo de dados, stack ou processo de aprovação DEVE ser registrada como ADR em `/docs/adr/`.
- Formato de nome de arquivo (obrigatório, numeração sequencial, nunca reaproveitar número de ADR removido/supersedido):

```
/docs/adr/ADR-<NNNN>-<slug-em-ingles>.md
```

  Exemplo: `/docs/adr/ADR-0006-timeout-bot-teams.md`. `NNNN` é o próximo inteiro disponível (4 dígitos, zero-padded), determinado lendo o maior número existente em `/docs/adr/`.

- Um agente DEVE criar ou atualizar um ADR quando:
  - Uma decisão altera um dos 4 componentes da arquitetura (pipeline de ingestão, API do assistente, bot Teams, painel web) de forma que afeta outro componente ou contrato entre eles.
  - Uma decisão de escopo remove, adia ou substitui um requisito já aprovado em `requirements.md`.
  - A decisão envolve trade-off relevante de custo, segurança, LGPD/compliance ou modelo de LLM (ex.: troca de GPT-4o por outro modelo).
- Um agente NÃO deve criar ADR quando:
  - For apenas uma correção de bug sem mudança de contrato ou comportamento documentado.
  - For um detalhe de implementação já coberto por um `plan.md` existente e sem impacto em outro componente.
  - For uma alteração cosmética de UI no painel web sem mudança de fluxo ou contrato.
- Ao atualizar uma decisão anterior, o agente cria um NOVO ADR referenciando o antigo como `Supersedes: ADR-NNNN`, e marca o ADR antigo com status `Superseded by ADR-NNNN`. Nunca editar o conteúdo de um ADR já aprovado além de seu campo de status.

### 3. Validation Gates (formato consumível por agente)

```yaml
validation_gates:
  - id: gate-1-spec-plan
    transicao: "requirements.md -> plan.md"
    aprovador: "Product Specialist"
    pre_condicao: "requirements.md existe em /specs/<modulo>/<spec-slug>/ e está completo"
    artefato_bloqueado: "plan.md"
    label_gate: "gate-1-spec-plan"
  - id: gate-2-tasks-implement
    transicao: "tasks.md -> implementação (código)"
    aprovador: "Tech Lead"
    pre_condicao: "tasks.md existe em /specs/<modulo>/<spec-slug>/ e foi aprovado pelo TL"
    artefato_bloqueado: "código de implementação / branch de feature"
    label_gate: "gate-2-tasks-implement"
  - id: gate-3-code-merge
    transicao: "code review -> merge"
    aprovador: "Tech Lead (code review) + 1 approval de PR"
    pre_condicao: "PR aberto referencia a task e a spec de origem"
    artefato_bloqueado: "merge para branch principal"
    label_gate: "gate-3-code-merge"
  - id: gate-4-tests-deploy
    transicao: "testes -> deploy"
    aprovador: "QA (cobertura e cenários) + Tech Lead (aprovação final de deploy)"
    pre_condicao: "suite de testes executada e cenários de QA documentados"
    artefato_bloqueado: "deploy (Bicep/pipeline de release)"
    label_gate: "gate-4-tests-deploy"
```

**Instrução explícita ao agente:** nunca gerar, avançar ou marcar como concluído um artefato de uma fase posterior (plan.md, tasks.md, PR de código, ou deploy) sem que o gate correspondente tenha sido satisfeito e a label `gate-atual` da task tenha sido atualizada para refletir isso. Se o gate anterior não estiver satisfeito, o agente DEVE parar e sinalizar qual aprovação está faltando, em vez de assumir aprovação implícita.

### 4. Restrições de Comunicação em Artefatos Gerados

| Tipo de artefato | Idioma/tom |
|---|---|
| Título e corpo de tasks/issues | Português |
| Documentos de status, relatórios de progresso, atas | Português |
| requirements.md, plan.md, tasks.md (specs) | Português |
| ADRs (título do arquivo em inglês, conteúdo em português) | Nome do arquivo em inglês; corpo em português |
| Código-fonte: nomes de variáveis, funções, classes | Inglês |
| Comentários no código | Inglês |
| Mensagens de commit | Inglês, formato `<tipo>(<módulo>): <descrição>` (ex.: `fix(bot-teams): corrige timeout em respostas longas`), seguindo Conventional Commits |
| Título e descrição de Pull Requests | Inglês no título; descrição pode ser em inglês ou português, mas deve referenciar a task e a spec de origem |

Regra adicional: nunca misturar idiomas dentro do mesmo campo (ex.: título de commit metade em português, metade em inglês). Em caso de dúvida sobre qual convenção se aplica a um artefato não listado acima, o agente deve tratá-lo como documentação de gestão e usar português.

## Build & Deploy
<!-- TODO (Tech Lead — Ex. 2.1) -->
