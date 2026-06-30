## Avaliação do Exercício 1.2

### Resumo
O participante entregou um e‑mail claro e acessível que ajusta expectativas e propõe critérios mensuráveis; entretanto faltou o one‑pager exigido (Claude Cowork) e não há evidência de iteração com a ferramenta nem histórico de refinamento.

### Scores por Dimensão

| Dimensão | Score | Justificativa |
|----------|-------|---------------|
| D1 — Domínio Conceitual | 2 | Explicação correta e acessível de RAG e dependência da qualidade das fontes ("entrada ruim leva a saída ruim"); porém falta menção a riscos técnicos específicos esperados pelo exercício (ex.: contexto rot, conflito de versões entre documentos). |
| D2 — Uso de Ferramentas | 1 | Não há evidência de uso do `Claude Cowork` para gerar o one‑pager nem de iteração/rodadas de refinamento (v1→v2). O arquivo `exercicio-02-prompt.txt` registra apenas salvar o e‑mail e exportar a conversa. |
| D3 — Qualidade do Entregável | 2 | O e‑mail é utilizável e contém critérios mensuráveis (bom), mas o entregável está incompleto: o one‑pager visual exigido não foi incluído. |
| D4 — Pensamento Crítico | 2 | O texto demonstra julgamento (validação do entusiasmo, critérios e próximo passo concreto), mas não há prova de análise humana anterior a uso de IA nem de iteração crítica do output da ferramenta. |
| D5 — Aplicabilidade ao Projeto | 3 | Mensagem alinhada ao contexto NovaTech (explica RAG, impacto da documentação, propõe reunião para priorizar 30–50 fontes), critérios propostos são relevantes e mensuráveis. |

**Score do exercício: 2.0**

### Verificação de Armadilhas
- Armadilhas intencionais no exercício: Nenhuma armadilha neste exercício.
- Itens obrigatórios não identificados: ausência do one‑pager gerado pelo Cowork (requisito do enunciado) — contabilizado como falta no entregável.

### Pontos Fortes
- Linguagem clara e acessível: analogia de “colega experiente” e explicação simples de RAG atende ao público executivo.
- Critérios de sucesso mensuráveis e relevantes (ex.: % respostas com fonte, % encaminhamentos, redução de tempo).
- Próximo passo prático sugerido (reunião para priorizar 30–50 fontes) demonstra orientação operacional.

### Pontos de Melhoria
- Incluir o one‑pager visual exigido (Claude Cowork). Ação: gerar um one‑pager com fluxo simplificado e anexá‑lo ao e‑mail.
- Evidenciar uso de ferramentas e iteração: anexar o histórico da conversa com Claude mostrando pelo menos 2 rodadas de refinamento (v1→v2) e o comando usado para Cowork.
- Tornar a explicação de riscos mais específica ao projeto: mencionar contexto rot, orçamento de atenção (volume de docs), e estratégia de versionamento/priorização como mitigação acionável.

### Classificação
Aprovado (2.0)

### Tópicos da Trilha para Reforço
- Engenharia de Contexto / Context rot (impacto do volume de documentação sobre qualidade das respostas).
- Pipeline de RAG: versão de documentos, priorização e métricas de confiança.
- Uso efetivo de ferramentas colaborativas (Claude Cowork) e práticas de iteração (gerar → avaliar → refinar) — evidenciar histórico ao entregar.
