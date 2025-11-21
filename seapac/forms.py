from django.forms import ModelForm
from django import forms
from .models import Family, Project, Technician, Subsystem, TimelineEvent
from django.forms import formset_factory, BaseFormSet
import json
from PIL import Image


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "nome_projeto": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "stle": "max-width:400px;"}
            ),
            "tecnicos": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 5}
            ),
            "familias": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 5}
            ),
            "orcamento": forms.TextInput(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
        }


class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
        fields = "__all__"
        widgets = {
            "nome_tecnico": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "especialidade": forms.Select(attrs={"class": "form-control"}),
        }


class FamilyForm(ModelForm):
    class Meta:
        model = Family
        exclude = ["terra", "subsistemas"]
        fields = "__all__"
        widgets = {
            "nome_titular": forms.TextInput(attrs={"class": "form-control"}),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "contato": forms.TextInput(attrs={"class": "form-control"}),
            "municipio": forms.Select(attrs={"class": "form-control"}),
            "projetos": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 5}
            ),
        }


class ProdutoForm(forms.Form):
    nome = forms.CharField(label="Nome do Produto", required=True)
    qtd = forms.FloatField(label="Quantidade", required=False)
    und = forms.CharField(label="Unidade de Medida", required=False)
    custo = forms.FloatField(label="Custo", required=False)
    valor = forms.FloatField(label="Valor Unitário", required=False)
    valor_potencial = forms.FloatField(label="Valor Potencial", required=False)
    destino = forms.CharField(label="Destino", required=False)
    descricao = forms.CharField(label="Descrição (Mundo Externo)", required=False)


ProdutoFormSet = formset_factory(ProdutoForm, extra=1)


class FluxoForm(forms.Form):
    nome_produto = forms.ChoiceField(choices=(), required=True, label="Produto")
    qtd = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Qtd"
    )
    und = forms.CharField(required=False, label="Unidade de Medida")
    custo = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Custo"
    )
    valor = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Valor Unitário"
    )
    valor_potencial = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2, label="Valor Potencial"
    )
    destino = forms.ChoiceField(choices=(), required=False, label="Destino")
    DELETE = forms.BooleanField(required=False)


class BaseFluxoFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        produtos_fluxos = {}
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                nome = form.cleaned_data.get("nome_produto")
                if not nome:
                    continue
                destino = form.cleaned_data.get("destino") or ""

                produtos_fluxos.setdefault(nome, []).append(
                    {
                        "destino": (
                            destino.strip() if isinstance(destino, str) else destino
                        )
                    }
                )

        erros = []
        for nome_produto, lista in produtos_fluxos.items():
            destinos = [item["destino"] for item in lista if item["destino"]]
            duplicados = set(d for d in destinos if destinos.count(d) > 1)
            if duplicados:
                erros.append(
                    f"O produto '{nome_produto}' tem destinos duplicados: {', '.join(sorted(duplicados))}."
                )


class SubsystemForm(forms.ModelForm):
    produtos_base = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Digite um produto por linha:\nCarne\nLeite\nEsterco",
                "rows": 5,
            }
        ),
        label="Produtos Base",
    )

    class Meta:
        model = Subsystem
        fields = [
            "nome_subsistema",
            "descricao",
            "produtos_base",
            "foto_subsistema",
            "tipo",
        ]
        widgets = {
            "nome_subsistema": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control"}),
            "foto_subsistema": forms.FileInput(attrs={"class": "form-control"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
        }

    # Função para validar o tipo de imagem enviada pelo usuário
    def clean_foto_subssistema(self):
        foto = self.cleaned_data.get("foto_subsistema")

        # Caso o usuário não envie nada (edição sem trocar a foto), retorna normal
        if not foto:
            return foto

        # Verificar a extensão permitida
        extensoes_validas = [".jpg", ".jpeg", ".png"]
        import os

        ext = os.path.splitext(foto.name)[1].lower()
        if ext not in extensoes_validas:
            raise forms.ValidationError(
                "Envie uma imagem nos formatos JPG, JPEG ou PNG."
            )

        # Verificar se o arquivo é realmente uma imagem
        try:
            img = Image.open(foto)
            img.verify()  # verifica estrutura interna

        except Exception:
            raise forms.ValidationError("O arquivo enviado não é uma imagem válida.")

        return foto

    def clean_produtos_base(self):
        data = self.cleaned_data.get("produtos_base", "")

        if isinstance(data, str) and data.strip().startswith("["):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                raise forms.ValidationError(
                    "JSON inválido. Use uma lista ou uma linha por produto."
                )

        linhas = [linha.strip() for linha in str(data).splitlines() if linha.strip()]
        produtos = [{"nome": linha, "fluxos": []} for linha in linhas]

        return produtos


class TimelineEventForm(ModelForm):
    class Meta:
        model = TimelineEvent
        exclude = ("family",)
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "data": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "secao": forms.TextInput(attrs={"class": "form-control"}),
        }
