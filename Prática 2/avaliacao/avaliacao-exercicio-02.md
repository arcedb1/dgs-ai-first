## Avaliação do Exercício 2.2 — Governança de specs no modelo SDD

### Resumo
Entregável muito sólido: dois documentos de governança bem estruturados (RACI, versionamento por status em vez de semântico, gates, changelog auditável), um board Kanban HTML funcional e fiel ao enunciado, e evidência real de iteração com uso do skill `the-fool` para red-team do change management, com melhorias efetivamente implementadas no documento. É o tipo de entregável que um outro membro do time usaria sem pedir esclarecimentos.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|----------------|
| D1 — Domínio Conceitual | 3 | Trata specs explicitamente como artefatos vivos (não documentos congelados), distingue versionamento por status vs. semântico com justificativa própria, e aplica corretamente o conceito de "dono natural aprova" ao SDD (Product Specialist/Tech Lead/Dev). Nuance clara ao explicar por que Copilot só entra em `tasks.md` (execução, não escopo/arquitetura). |
| D2 — Uso de Ferramentas | 3 | Evidência real de iteração documentada em `02-exercicio-prompt3.txt`: prompt inicial → análise crítica via `/the-fool` (modo socrático) → pedido de "visão mais realista" → implementação seletiva dos itens 1, 3 e 5 das melhorias sugeridas (com justificativa explícita de por que 2 e 4 ficaram de fora). Não é aceitação acrítica — há reescrita real do documento entre versões. Cowork usado para gerar o board com pergunta de formato e entrega funcional. |
| D3 — Qualidade do Entregável | 3 | Completo, correto e acionável: RACI consolidado, esquema de cabeçalho de status, estrutura de repositório alinhada ao Anexo C, exemplo aplicado passo a passo (CR-014, feedback-api). O board é de fato "machine-readable"/utilizável — HTML funcional com drag-and-drop, filtros e persistência, testado (arquivo íntegro, 181 linhas, sem erros aparentes). |
| D4 — Pensamento Crítico | 3 | Identifica limitações reais do próprio processo: dependência de disciplina humana sem CI bloqueante, Tech Lead como ponto único de falha, risco de auto-classificação de impacto sob pressão de prazo. Documenta explicitamente o que foi aceito e o que foi conscientemente deixado como trade-off ("registrados como trade-offs conscientes, não corrigidos no texto a pedido do usuário"). Confiança da síntese declarada como "MEDIUM", com teste sugerido para validar na prática. |
| D5 — Aplicabilidade ao Projeto | 3 | Usa os 5 módulos do NovaTech, referencia ADRs (`docs/adr/0001-escolha-azure-openai.md`), aponta para o checklist de validation gates já existente no projeto (`01-checklist-validation-gates.md`) e replica a estrutura do Anexo C fielmente (specs espelhando `/src/`). |

**Score do exercício: 3.0**

### Verificação de Artefatos Machine-Readable
O board HTML é de fato utilizável, não apenas ilustrativo: estrutura de dados em JS (array `seed`), drag-and-drop funcional que persiste via `localStorage`, filtros por responsável/artefato e busca textual. Os documentos de governança são prescritivos onde importa (regras de "nunca" e "sempre", tabelas RACI, cabeçalho YAML padronizado para status) — não é só narrativa.

### Pontos Fortes
- Iteração real e transparente: usa `/the-fool` para desafiar o próprio documento e implementa correções seletivas com justificativa, em vez de aceitar a primeira versão.
- Trata explicitamente casos de borda do mundo real (Tech Lead indisponível, task já mesclada quando CR chega, conflito de interesse na auto-classificação de impacto).
- Exemplo aplicado ponta a ponta (CR-014) amarra teoria e prática, mostrando propagação em cascata e efeito em board/tasks.

### Pontos de Melhoria
- O mecanismo de verificação da regra de ouro (nenhuma task codada contra spec não aprovada) depende de um campo declarado no PR, não de enforcement técnico (CI/hook) — o próprio autor reconhece essa fragilidade, mas seria valioso propor ao menos um esboço de automação futura (ex.: script de CI que compara status do cabeçalho da spec com a branch).
- Itens 2 e 4 da análise crítica (backup de aprovador estendido ao CM; SLA de task pós-merge crítica) ficaram de fora por decisão do usuário — está bem documentado, mas vale registrar como débito técnico explícito para não se perder.

### Classificação
Aprovado com distinção (3.0)

### Tópicos da Trilha para Reforço
Nenhum — entregável no nível esperado para certificação.
