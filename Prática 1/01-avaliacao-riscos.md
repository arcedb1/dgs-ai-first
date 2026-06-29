## Documento de avaliação de riscos técnicos de IA

### 1. Contexto resumido

NovaTech quer reduzir o tempo médio de busca de 12 para menos de 2 minutos por chamado a partir de um assistente de IA integrado ao Teams + SharePoint. O projeto cobre 1.250 fontes de documentação internas em Microsoft 365, Confluence e rede local, com atualização recorrente e sem processo de revisão unificado. Há PII básico nos documentos e o objetivo é que o assistente só ofereça decisão final ao atendente quando houver conflitos entre versões.

---

### 2. Riscos técnicos principais

#### Risco 1 — Alucinação
- Probabilidade: **Alta**
- Impacto:
  - Prazo: **Médio/Alto** — correções de respostas falsas e ajustes de comportamento do modelo podem demandar semanas extras.
  - Custo: **Médio** — exige envolvimento de especialista de domínio para refinar fallback e validação de respostas.
  - Qualidade: **Alto** — perda de confiança e risco de indicação de procedimentos inexistentes.
- Mitigações acionáveis:
  1. Exigir que toda resposta seja apoiada por citação explícita de fonte (documento + trecho/URL). Se não houver evidência sólida, o sistema responde “não encontrei evidência consistente”.
  2. Implantar detecção de inconsistência no RAG: quando múltiplos documentos retornados não concordam, produzir um fallback de conflito em vez de uma resposta única.
  3. Adotar regras de rejeição automática por score de similaridade: respostas geradas abaixo do limiar operacional não devem ser apresentadas como certezas.

#### Risco 2 — Documentação contraditória entre versões
- Probabilidade: **Alta**
- Impacto:
  - Prazo: **Médio** — demanda tempo extra em discovery e modelagem de metadados de versão.
  - Custo: **Médio** — precisa de validação contínua por área de negócios e ajustes no pipeline.
  - Qualidade: **Alto** — atendente pode receber instrução errada se o sistema misturar versões.
- Mitigações acionáveis:
  1. Capturar metadados de versão/data/responsável durante a ingestão e persistir no índice.
  2. Aplicar regra de priorização rígida no RAG: escolher preferencialmente documentos mais recentes ou ativos conforme política de governança.
  3. Sempre exibir conflito ao atendente quando há versões divergentes, deixando a decisão final com ele.
  4. Incluir tags de “obsoleto”/“em revisão” no índice para filtrar respostas por documentos ativos.

#### Risco 3 — Dependência da qualidade dos documentos-fonte
- Probabilidade: **Alta**
- Impacto:
  - Prazo: **Médio** — requer classificação, limpeza e padronização antes da indexação.
  - Custo: **Médio** — envolve curadoria, ETL, processamento de OCR e ajustes de extração de texto.
  - Qualidade: **Alto** — resultados são tão bons quanto as fontes; conteúdo ruim reduz acurácia.
- Mitigações acionáveis:
  1. Definir critérios mínimos de ingestão: só indexar documentos com título claro, data e fonte identificados; demais vão para fila de revisão.
  2. Automatizar validação de qualidade no pipeline: detectar texto extraível fraco, OCR ruim ou HTML quebrado e rejeitar/encaixar para revisão.
  3. Fazer revisão de amostra de 10-15% dos documentos por área antes do go-live; se >20% falhar, ajustar o pipeline.
  4. Criar score de qualidade de documento que impacte ranking de resposta, priorizando fontes de maior qualidade.

#### Risco 4 — Expectativa da diretoria vs. entrega atual da tecnologia
- Probabilidade: **Alta**
- Impacto:
  - Prazo: **Médio/Alto** — escopo pode precisar ser reduzido ou recalibrado se a diretoria esperar ganhos imediatos e completos.
  - Custo: **Médio** — inclui risco do preço do token/consulta da API Azure AI ultrapassar o ganho de tempo dos atendentes, tornando o projeto economicamente ineficiente.
  - Qualidade: **Médio** — pressa por resultados pode gerar MVP frágil e com UX de baixa confiança.
- Mitigações acionáveis:
  1. Definir entregáveis de MVP claros antes do início: por exemplo, “responder 60% das consultas críticas com citação e reduzir tempo de busca em 30% no piloto”.
  2. Fazer PoC de 2 semanas com dados reais e medir redução de tempo de busca em um grupo piloto.
  3. Comunicar explicitamente que a solução inicial é “assistente de consulta com evidência”, não um substituto total de consultoria de processo.
  4. Estabelecer métricas de aceitação concretas: uso, precisão de citação, satisfação e redução de tempo em vez de promessas genéricas.

#### Risco 5 — Context rot por volume grande de documentação
- Probabilidade: **Média/Alta**
- Impacto:
  - Prazo: **Médio** — será preciso ajustar chunking, filtros e o fluxo de recuperação de contexto.
  - Custo: **Médio** — aumenta custo de índices, consultas e tokens para selecionar contexto relevante.
  - Qualidade: **Alto** — respostas podem se tornar ambíguas, citar fontes irrelevantes ou perder foco.
- Mitigações acionáveis:
  1. Segmentar o índice por área/assunto e, se possível, usar namespaces ou índices separados para reduzir o espaço de busca.
  2. Aplicar recall incremental com filtros de metadados antes do modelo, limitando a seleção a 3-5 documentos mais relevantes.
  3. Ajustar tamanho de chunk e overlap com base no tipo de documento, evitando diluição em conteúdo muito extenso.
  4. Medir drift de precisão periodicamente com queries representativas e reindexar ou refinar filtros quando o recall cair.

---

### 3. Síntese e recomendações para kickoff

- O maior risco imediato é a combinação de **alucinação + documentação contraditória**: isso exige foco em governança de fonte e em respostas baseadas em evidência.
- O projeto precisa de um **MVP limitado** e um **PoC rápido** para calibrar expectativas frente às metas agressivas da diretoria.
- A ingestão precisa ser tratada como **etapa de produto**, não apenas técnica: metadados, taxa de qualidade e classificação de versão devem ser parte do escopo de discovery.
- A economia do projeto deve ser avaliada não só em ganho de tempo, mas também em **custo de token/consulta** da Azure AI versus tempo de atendente.

---

### 4. Três perguntas para o Tech Lead

1. O que vamos aceitar como critério mínimo de “documento indexável” no MVP? (ex: título/data/fonte obrigatórios, documentos em revisão excluídos)
2. Como queremos tratar conflitos entre versões na interface do atendente: apenas exibir as fontes conflitantes ou também oferecer um resumo de “pontos divergentes”?
3. Qual é o limite de custo por usuário/mês para Azure AI, considerando o volume previsto, antes de precisarmos rever o modelo de implantação ou o escopo do assistente?
