# seapac/reports/graficos.py

import io
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def grafico_producao(produtos):
    nomes = [p["produto"] for p in produtos]
    qtd = [p["qtd"] for p in produtos]

    fig, ax = plt.subplots(figsize=(5.5, 3))
    ax.bar(nomes, qtd)
    ax.set_title("Produção total por produto")
    ax.set_ylabel("Quantidade")
    ax.tick_params(axis="x", rotation=45)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def grafico_receita_real_potencial(produtos):
    nomes = [p["produto"] for p in produtos]
    receita_real = [p["receita"] for p in produtos]
    receita_pot = [p["receita_potencial"] for p in produtos]

    fig, ax = plt.subplots(figsize=(5.5, 3))

    x = range(len(nomes))
    ax.bar(x, receita_real, label="Receita Real")
    ax.bar(x, receita_pot, bottom=receita_real, label="Receita Potencial")

    ax.set_xticks(x)
    ax.set_xticklabels(nomes, rotation=45)
    ax.set_title("Receita real x Receita potencial")
    ax.legend()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf
