## 1. Linha entre “IA cataloga” e “humano decide"

- A IA deve assumir tarefas baseadas em leitura em massa, estruturação e detecção de padrões: catalogar fontes, agrupar por tema, apontar conflitos e gaps, identificar dependências extraídas da documentação.
- Humanos devem assumir julgamento de negócio, validação de contexto e decisões de prioridade: escolher quais gaps são relevantes, confirmar critérios de governança, decidir escopo do MVP e priorizar entregáveis.
- Em termos práticos:
  - IA entrega insumos e recomendações baseadas em evidência objetiva.
  - Humanos usam esses insumos para decisões de valor, risco e governança.

---

## 2. Plano de discovery

### 2.1 Atividades executadas por agentes de IA (fase de Intent)

**[PRÉ-REQUISITO] Validação de cobertura e qualidade dos canais de ingestão**
   - Output: relatório de readiness com taxa de cobertura por fonte, tipos de documento não processáveis, bloqueios de acesso identificados e plano de correção técnica.
   - Sem este pré-requisito, as etapas subsequentes podem gerar inventário incompleto ou comprometido.

1. Catalogar o conjunto de ~1.250 documentos
   - Output: inventário com metadados padrão por fonte, tipo de documento, última atualização, autor/responsável, estado aparente.
2. Normalizar e reconciliar fontes
   - Output: mapa de origem único com contagem por SharePoint, Confluence e rede local, identificando fontes não acessíveis ou formatos incompatíveis.
   - Critério de aceitação: ≥ X% de cobertura de fontes esperadas (a definir com cliente).
3. Identificar duplicatas e versões conflitantes
   - Output: lista de documentos duplicados, versões múltiplas e evidências de divergência de conteúdo entre versões.
4. Classificar temas e processos recorrentes
   - Output: taxonomia preliminar de temas/processos, junto de frequência e cobertura documental.
5. Mapear dependências entre sistemas/processos citados
   - Output: grafo de dependências extraídas da documentação (sistemas, fluxos, atores, regras de negócio).
6. **Gerar glossário inicial e ontologia de termos**
   - Output: dicionário estruturado de termos-chave e definições extraídas da documentação, com indicadores de ambiguidade ou conflito de definições.
   - Propósito: reduzir ruído nas entrevistas e garantir que o MVP use linguagem consistente.
7. Detectar gaps de documentação
   - Output: lista preliminar de temas/processos com baixa cobertura documental ou ausência de respostas claras.
8. Identificar riscos de qualidade de fonte
   - Output: score ou etiqueta de qualidade por documento, apontando OCR ruim, texto incompleto, títulos ausentes ou metadados insuficientes.
9. Extrair cláusulas de governança existentes
   - Output: inventário de políticas, regras de versão, status de documento e indicadores de obsolescência presentes na documentação.
   - Critério: classificar como "governo-pronto" vs "falta de padrão de versão".
10. **IA-assisted stakeholder mapping**
    - Output: lista de perfis, áreas de responsabilidade e atores citados nos documentos, com recomendação de quem deve ser entrevistado e em qual sequência.
    - Propósito: orientar priorização de entrevistas.
11. Gerar resumo executivo de contexto
    - Output: relatório de "estado da base documental" com principais temas, lacunas críticas, riscos de inconsistência e volumes por fonte.
12. **Produzir um mapa de prioridades sugeridas**
    - Output A (técnico): priorização por volume, conflitos detectados e qualidade de fonte.
    - Output B (negócio): cruzamento com modelo de impacto comercial — uso em SLA, frequência de chamados, risco operacional — a definir com sponsor executivo.
    - Produto final: matriz 2x2 (impacto-vs-cobertura) para guiar foco do MVP.
13. **Teste rápido de RAG com 2-3 consultas críticas**
    - Output: validação piloto de que a base documental consegue suportar respostas estruturadas com citação explícita.
    - Critério: se ≥ 70% das consultas críticas retornam resposta com citação válida, a base está pronta; caso contrário, recomendação de reforço de governança de fonte.
14. **Definir métricas de qualidade da Intent**
    - Output: gate de aceitação com critérios numéricos:
      - Cobertura mínima: ≥ X% de fontes cadastradas;
      - Confiabilidade de detecção: taxa de conflitos detectados validada por amostra humana ≥ Y%;
      - Número mínimo de gaps classificados por negócio.

### 2.2 Atividades executadas por humanos (discovery propriamente dito)

1. Validar e ajustar o inventário gerado pela IA
   - Uso do output da IA como referência para confirmar acessos corretos, fontes relevantes e documentos críticos.
2. Conduzir entrevistas com stakeholders-chave
   - Guiadas pelo mapa de gaps e temas da IA, focando em:
     - quais processos são críticos no negócio
     - onde a documentação atual falha na prática
     - níveis de confiança esperados para respostas do assistente
3. Confirmar prioridades de processos e casos de uso
   - Decidir quais temas/documentos devem ser tratados no MVP e quais podem ficar para fases posteriores.
4. Revisar conflitos e versões relevantes
   - Avaliar se os conflitos detectados pela IA representam riscos reais de operação ou apenas versões corrigidas/obsoletas.
5. Definir critérios mínimos de governança documental
   - Aprovar quais metadados são obrigatórios, como tratar versões e quando um documento deve ser excluído do índice.
6. **Priorizar gaps de conteúdo com co-responsabilidade IA/humano**
   - Processo: IA propõe gaps com classificação técnica → humanos classificam por impacto/risco de negócio → IA refina recomendações com foco em áreas validadas → validação final com sponsor executivo.
   - Saída: lista de gaps priorizada, vinculada a temas críticos do MVP.
7. Validar dependências críticas do negócio
   - Confirmar se o mapa de dependências é completo e se identifica os sistemas/processos que impactam o atendimento.
8. Alinhar expectativas de escopo e entregáveis
   - Estabelecer limites do piloto, métricas de sucesso e o conceito de “assistente de consulta com evidência”.
9. Analisar viabilidade de infraestrutura e acesso
   - Confirmar se os acessos identificados pela IA são suficientes e se há impedimentos técnicos ou políticas de segurança.
10. **Formalizar filtro de relevância de documento**
    - Critérios de inclusão/exclusão: atualidade, governança, relação a processos críticos, indexabilidade.
    - Output: política de indexação vinculada à aprovação de governança documental.
11. Aprovar o plano de discovery e o próximo backlog
    - Decidir quem aprova a priorização final de gaps e quais documentações serão ingestadas no MVP.

### 2.3 Sequência e dependências

1. Preparação de acessos e coleta inicial
   - Antes do início da fase de Intent, o cliente deve fornecer acessos e inventário de fontes.
2. **[PRÉ-REQUISITO] Validação técnica de ingesta**
   - Teste de extração de amostra de cada fonte (SharePoint, Confluence, pastas de rede).
   - Bloqueios de acesso e incompatibilidades de formato identificados e resolvidos.
3. Fase de Intent (IA)
   - Catalogação, normalização, identificação de conflitos/gaps, mapeamento de temas, dependências, stakeholders.
   - Geração de glossário, teste piloto de RAG.
   - Output principal: mapeamento de fontes, gaps e riscos documentais, prioridades técnicas e de negócio.
4. Revisão humana dos achados da IA
   - Validação dos dados, ajuste de prioridades e eliminação de falsos positivos.
   - Ciclo iterativo de priorização de gaps.
5. **[GATE DE ACEITAÇÃO DA INTENT]**
   - Critério de aprovação: cobertura ≥ X%, RAG test ≥ 70%, gaps classificados por negócio, glossário aprovado, stakeholder map validado.
   - Responsável: sponsor executivo.
   - **SEM ESTA APROVAÇÃO, não prosseguir para discovery humano guiado.**
6. Discovery humano guiado
   - Entrevistas e workshops baseados no mapa de gaps, glossário e stakeholder mapping da IA.
   - Foco: validação de prioridades, confirmação de processos críticos, alinhamento de expectativas.
7. Decisão de escopo e governança
   - Priorização final de gaps, definição de critérios de indexação e critério de "documento autorizado".
   - Aprovação de política de versão e obsolescência.
8. Planejamento do piloto de IA
   - Backlog do MVP definido com base em outputs validados.

> A fase de Intent alimenta e reduz o tempo do discovery humano, não o substitui.

---

## 3. O que a NovaTech precisa fornecer

1. Acessos de leitura antes do Dia 1
   - SharePoint com permissão de leitura para as bibliotecas relevantes.
   - Confluence com acesso de leitura aos espaços e páginas do projeto.
   - Pastas de rede/mapeamentos de arquivo com credenciais de leitura ou cópia dos arquivos.
2. Inventário inicial de fontes
   - Lista preliminar das 1.250 fontes esperadas, com priorização mínima se houver.
   - Políticas de retenção e versionamento já existentes.
3. Pessoas e tempo
   - 1 sponsor executivo para aprovar escopo e decisão de gaps.
   - 1 owner de conhecimento de processos logísticos.
   - 1 responsável por governança documental / compliance.
   - 1 representante de TI ou infraestrutura para confirmar acessos.
   - Tempo estimado: 2-3 horas por stakeholder na semana de validação, com foco em entrevistas guiadas pela IA.
4. Decisões
   - Quem aprova a priorização final de gaps e o critério de “documento indexável”.
   - Quem decide a fronteira do MVP e o conjunto inicial de temas críticos.
   - Critérios de sucesso do piloto (ex: redução de tempo de pesquisa, taxa de resposta com citação, acurácia operacional).
---

## 4. Gates de aceitação e métricas de qualidade da Intent

A fase de Intent só prossegue se os outputs atingem qualidade mínima aceitável. Recomenda-se:

### 4.1 Gate 1: Readiness técnico (pré-Intent)
- ✓ Cobertura de fontes: ≥ 90% das 1.250 fontes esperadas acessíveis
- ✓ Formatos compatíveis: ≥ 95% dos documentos extraíveis (excluindo binários puros)
- ✓ Amostra de teste: 3 consultas críticas retornam resultado com estrutura válida

### 4.2 Gate 2: Qualidade da Intent (pós-análise)
- ✓ Cobertura de ingestão: ≥ 85% de documentos classificados com metadados completos
- ✓ Consistência de gaps: validação manual de amostra (20-30 gaps) confirma ≥ 80% relevância
- ✓ Conflitos detectados: taxa de falsos positivos < 15% em amostra validada
- ✓ RAG test: ≥ 70% das consultas críticas retornam resposta com citação explícita
- ✓ Gloss­ário: ≥ 50 termos críticos definidos, sem ambiguidades não resolvidas
- ✓ Stakeholder map: todos os departamentos impactados identificados

### 4.3 Gate 3: Aprovação executiva (antes de entrevistas)
- ✓ Sponsor valida priorização final de gaps (matriz de impacto vs cobertura)
- ✓ Governança documental aprovada: critério de "documento autorizado" formalizado
- ✓ Escopo do piloto confirmado: temas críticos do MVP definidos

---

## 5. Considerações críticas e riscos residuais

1. **Alucinação em priorização**: a IA pode detectar "gaps" que não são realmente lacunas de negócio.
   - Mitigação: validação humana em amostra (20-30%) antes de aceitar a lista completa.

2. **Glossário incompleto ou enviesado**: termos extraídos podem não cobrir o domínio completo ou podem conflitar com uso real.
   - Mitigação: glossário é "preliminar"; humanos refinam durante entrevistas com stakeholders.

3. **Bloqueio de acesso tardio**: descobre-se durante a Intent que um compartilhamento crítico não é acessível.
   - Mitigação: validação técnica precede a fase de Intent; nenhum documento é garantido sem prova de extração prévia.

4. **Dependência de metadados inadequados**: SharePoint/Confluence podem não ter data de atualização ou responsável preenchidos.
   - Mitigação: rejeitar documento se metadados obrigatórios faltarem; encaminhar para curadoria antes de indexação.

5. **RAG test com amostra pequena**: 2-3 consultas podem não ser representativas.
   - Mitigação: consultas devem ser selecionadas com sponsor (10 principais perguntas de atendentes), não apenas aleatórias.

---

## 6. Próximos passos após este plano

1. **Kickoff com NovaTech**: validar pré-requisitos (acessos, pessoas, cronograma).
2. **Refinamento de critérios numéricos**: concordar com cliente em % de cobertura mínima, threshold de RAG, etc.
3. **Definição de sponsor executivo**: confirmação de quem aprova gates e decisões finais.
4. **Elaboração de script de entrevista**: preparar perguntas guiadas pelos gaps e gloss­ário da Intent.
5. **Cronograma detalhado**: alinhar duração real de cada phase com recursos disponíveis.