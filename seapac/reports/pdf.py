import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.utils import ImageReader

from .graficos import grafico_producao, grafico_receita_real_potencial


def gerar_relatorio_family(family):

    renda = family.calcular_renda()
    produtos = renda["produtos"]

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Relatório Agroecológico", styles["Title"]))
    story.append(Paragraph(f"Família: {family.nome_titular}", styles["Heading2"]))
    story.append(Paragraph(f"Município: {family.municipio.nome}", styles["Normal"]))
    story.append(Spacer(1, 0.4 * inch))

    graf1 = grafico_producao(produtos)
    story.append(Image(graf1, width=5.5 * inch, height=3 * inch))
    story.append(Spacer(1, 0.3 * inch))

    graf2 = grafico_receita_real_potencial(produtos)
    story.append(Image(graf2, width=5.5 * inch, height=3 * inch))
    story.append(Spacer(1, 0.3 * inch))

    tabela = [["Produto", "Qtd", "Receita", "Receita Potencial", "Custo", "Lucro"]]

    for p in produtos:
        tabela.append(
            [
                p["produto"],
                f"{p['qtd']:.2f}",
                f"{p['receita']:.2f}",
                f"{p['receita_potencial']:.2f}",
                f"{p['custo_total']:.2f}",
                f"{p['lucro']:.2f}",
            ]
        )

    story.append(Paragraph("Resumo dos Produtos", styles["Heading2"]))
    story.append(Table(tabela))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Resumo Geral", styles["Heading2"]))
    story.append(
        Paragraph(f"Receita Total: R$ {renda['total_receita']:.2f}", styles["Normal"])
    )
    story.append(
        Paragraph(
            f"Receita Potencial: R$ {renda['total_receita_potencial']:.2f}",
            styles["Normal"],
        )
    )
    story.append(
        Paragraph(f"Lucro Total: R$ {renda['renda_total']:.2f}", styles["Normal"])
    )
    story.append(
        Paragraph(
            f"Lucro Potencial: R$ {renda['renda_total_potencial']:.2f}",
            styles["Normal"],
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer
