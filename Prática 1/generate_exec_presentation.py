from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

output_path = r"c:\Users\adriano.passamani\OneDrive - DB1 Group\Documentos\treinamentos IA\dgs-ia-first\dgs-ai-first\Prática 1\01-avaliacao-riscos-executiva.pdf"

doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=0.6*inch, leftMargin=0.6*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='DB1Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor('#0F4C81'), spaceAfter=6))
styles.add(ParagraphStyle(name='DB1Subtitle', parent=styles['BodyText'], fontName='Helvetica', fontSize=10, leading=12, textColor=colors.HexColor('#4F4F4F'), spaceAfter=10))
styles.add(ParagraphStyle(name='DB1Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.2, leading=13, textColor=colors.HexColor('#1F1F1F'), spaceAfter=6))
styles.add(ParagraphStyle(name='DB1Bold', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=10.2, leading=13, textColor=colors.HexColor('#0F4C81'), spaceAfter=6))
styles.add(ParagraphStyle(name='DB1Bullet', parent=styles['BodyText'], fontName='Helvetica', fontSize=10.2, leading=13, textColor=colors.HexColor('#1F1F1F'), leftIndent=12, bulletIndent=0, spaceAfter=4))
styles.add(ParagraphStyle(name='DB1Callout', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=colors.HexColor('#0F4C81'), backColor=colors.HexColor('#EAF3FA'), borderPadding=8, spaceAfter=10))

story = []
story.append(Paragraph("Avaliação executiva de riscos técnicos — Assistente de IA RAG", styles['DB1Title']))
story.append(Paragraph("DB1 | IA & Data | Kickoff interno — NovaTech", styles['DB1Subtitle']))
story.append(Spacer(1, 6))

summary = Table([
    [Paragraph("Resumo executivo", styles['DB1Bold']), Paragraph("O projeto é viável, com governança documental, escopo bem delimitado e um piloto com métricas claras antes de escala.", styles['DB1Body'])]
], colWidths=[1.4*inch, 5.8*inch])
summary.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), colors.HexColor('#0F4C81')),
    ('TEXTCOLOR', (0,0), (0,0), colors.white),
    ('BACKGROUND', (1,0), (1,0), colors.HexColor('#F4F8FB')),
    ('GRID', (0,0), (1,0), 0.5, colors.HexColor('#D8E7F3')),
    ('VALIGN', (0,0), (1,0), 'MIDDLE'),
    ('PADDING', (0,0), (1,0), 8),
]))
story.append(summary)
story.append(Spacer(1, 8))

story.append(Paragraph("Principais riscos e implicações", styles['DB1Bold']))
risks = [
    [Paragraph("1. Alucinação e confiabilidade", styles['DB1Bold']), Paragraph("Respostas sem evidência podem induzir procedimentos incorretos; exige citação obrigatória e fallback humano quando a confiança for baixa.", styles['DB1Body'])],
    [Paragraph("2. Contradição de versões", styles['DB1Bold']), Paragraph("Documentos divergentes podem gerar respostas conflitantes; é necessário metadados de versão, priorização e visibilidade explícita do conflito ao atendente.", styles['DB1Body'])],
    [Paragraph("3. Qualidade da base documental", styles['DB1Bold']), Paragraph("O desempenho do RAG depende diretamente da qualidade dos documentos-fonte; sem governança e revisão, o custo de manutenção cresce rapidamente.", styles['DB1Body'])],
]
rt = Table(risks, colWidths=[1.8*inch, 5.4*inch], repeatRows=1)
rt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#D8E7F3')),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('PADDING', (0,0), (-1,-1), 6),
]))
story.append(rt)
story.append(Spacer(1, 8))

story.append(Paragraph("Recomendações prioritárias", styles['DB1Bold']))
story.append(Paragraph("• Criar governança documental com dono por fonte, ciclo de revisão, regra de versão e status do documento (ativo, em revisão, obsoleto).", styles['DB1Bullet']))
story.append(Paragraph("• Transformar o PoC em um piloto de negócio com métricas concretas: tempo médio de resolução, taxa de resposta correta com citação, intervenção humana e custo por consulta.", styles['DB1Bullet']))
story.append(Paragraph("• Implementar fallback explícito para conflito ou baixa confiança, encaminhando a decisão para a equipe humana.", styles['DB1Bullet']))

story.append(Spacer(1, 8))
story.append(Paragraph("Decisão executiva: avançar apenas com escopo controlado e prova de valor objetiva.", styles['DB1Callout']))

doc.build(story)
