from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subsystem, FamilySubsystem


@receiver(post_save, sender=Subsystem)
def atualizar_familias_com_novos_produtos(sender, instance, **kwargs):
    subsistema = instance
    produtos_base = subsistema.produtos_base or []

    for fs in FamilySubsystem.objects.filter(subsystem=subsistema):
        produtos_saida = fs.produtos_saida or []
        nomes_existentes = {p["nome"] for p in produtos_saida}

        # adiciona novos produtos
        novos_produtos = []
        for produto in produtos_base:
            nome = produto.get("nome") if isinstance(produto, dict) else produto
            if nome not in nomes_existentes:
                novos_produtos.append({"nome": nome, "fluxos": []})

        # remove produtos que não estão mais no base
        nomes_produtos_base = {
            p.get("nome") if isinstance(p, dict) else p for p in produtos_base
        }
        fs.produtos_saida = [
            p
            for p in (fs.produtos_saida + novos_produtos)
            if p["nome"] in nomes_produtos_base
        ]

        fs.save()
