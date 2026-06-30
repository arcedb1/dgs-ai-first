## 1. Linha entre “IA cataloga” e “humano decide"

- A IA deve assumir tarefas baseadas em leitura em massa, estruturação e detecção de padrões: catalogar fontes, agrupar por tema, apontar conflitos e gaps, identificar dependências extraídas da documentação.
- Humanos devem assumir julgamento de negócio, validação de contexto e decisões de prioridade: escolher quais gaps são relevantes, confirmar critérios de governança, decidir escopo do MVP e priorizar entregáveis.
- Em termos práticos:
  - IA entrega insumos e recomendações baseadas em evidência objetiva.
  - Humanos usam esses insumos para decisões de valor, risco e governança.

---

## 2. Plano de discovery

### 2.1 Atividades executadas por agentes de IA (fase de Intent)

1. Catalogar o conjunto de ~1.250 documentos
   - Output: inventário com metadados padrão por fonte, tipo de documento, última atualização, autor/responsável, estado aparente.
2. Normalizar e reconciliar fontes
   - Output: mapa de origem único com contagem por SharePoint, Confluence e rede local, identificando fontes não acessíveis ou formatos incompatíveis.
3. Identificar duplicatas e versões conflitantes
   - Output: lista de documentos duplicados, versões múltiplas e evidências de divergência de conteúdo entre versões.
4. Classificar temas e processos recorrentes
   - Output: taxonomia preliminar de temas/processos, junto de frequência e cobertura documental.
5. Mapear dependências entre sistemas/processos citados
   - Output: grafo de dependências extraídas da documentação (sistemas, fluxos, atores, regras de negócio).
6. Detectar gaps de documentação
   - Output: lista preliminar de temas/processos com baixa cobertura documental ou ausência de respostas claras.
7. Identificar riscos de qualidade de fonte
   - Output: score ou etiqueta de qualidade por documento, apontando OCR ruim, texto incompleto, títulos ausentes ou metadados insuficientes.
8. Extrair cláusulas de governança existentes
   - Output: inventário de políticas, regras de versão, status de documento e indicadores de obsolescência presentes na documentação.
9. Gerar resumo executivo de contexto
   - Output: relatório de “estado da base documental” com principais temas, lacunas críticas, riscos de inconsistência e volumes por fonte.
10. Produzir um mapa de prioridades sugeridas
    - Output: proposta inicial de priorização de fontes e temas para entrevistas, baseada em volume, criticidade e conflitos detectados.

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
6. Priorizar gaps de conteúdo
   - Decidir quais lacunas documentais representam necessidades de negócio versus ruído analítico.
7. Validar dependências críticas do negócio
   - Confirmar se o mapa de dependências é completo e se identifica os sistemas/processos que impactam o atendimento.
8. Alinhar expectativas de escopo e entregáveis
   - Estabelecer limites do piloto, métricas de sucesso e o conceito de “assistente de consulta com evidência”.
9. Analisar viabilidade de infraestrutura e acesso
   - Confirmar se os acessos identificados pela IA são suficientes e se há impedimentos técnicos ou políticas de segurança.
10. Aprovar o plano de discovery e o próximo backlog
    - Decidir quem aprova a priorização final de gaps e quais documentações serão ingestadas no MVP.

### 2.3 Sequência e dependências

1. Preparação de acessos e coleta inicial
   - Antes do início da fase de Intent, o cliente deve fornecer acessos e inventário de fontes.
2. Fase de Intent (IA)
   - Catalogação, normalização, identificação de conflitos/gaps, mapeamento de temas e dependências.
   - Output principal: mapeamento de fontes, gaps e riscos documentais.
3. Revisão humana dos achados da IA
   - Validação dos dados, ajuste de prioridades e eliminação de falsos positivos.
4. Discovery humano guiado
   - Entrevistas e workshops baseados no mapa de gaps e temas.
5. Decisão de escopo e governança
   - Priorização final de gaps, definição de critérios de indexação e critério de “documento autorizado”.
6. Planejamento do piloto de IA
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
   - 1 dono de conhecimento de processos logísticos.
   - 1 responsável por governança documental / compliance.
   - 1 representante de TI ou infraestrutura para confirmar acessos.
   - Tempo estimado: 2-3 horas por stakeholder na semana de validação, com foco em entrevistas guiadas pela IA.
4. Decisões
   - Quem aprova a priorização final de gaps e o critério de “documento indexável”.
   - Quem decide a fronteira do MVP e o conjunto inicial de temas críticos.
   - Critérios de sucesso do piloto (ex: redução de tempo de pesquisa, taxa de resposta com citação, acurácia operacional).