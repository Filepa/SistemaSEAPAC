from django import forms
from django.forms import ModelForm, formset_factory, BaseFormSet
from .models import Family, Project, Technician, Subsystem, TimelineEvent
from .validators import validate
from PIL import Image
import re
import json
import os


# ---------------------------
# PROJECT
# ---------------------------
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = "__all__"
        labels = {
            "nome_projeto": "Nome do Projeto",
            "descricao": "Descrição",
            "tecnicos": "Técnicos",
            "familias": "Famílias",
            "orcamento": "Orçamento (R$)",
            "data_inicio": "Data de Início",
            "data_fim": "Data de Finalização",
            "status": "Status",
        }
        widgets = {
            "nome_projeto": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o nome do projeto",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descreva o projeto",
                }
            ),
            "tecnicos": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 6}
            ),
            "familias": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 6}
            ),
            "orcamento": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "0.00"}
            ),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "data_fim": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ProjectEditForm(ProjectForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (
            self.instance
            and self.instance.pk
            and getattr(self.instance, "orcamento", None) is not None
        ):
            self.initial["orcamento"] = self.instance.orcamento

    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
            if "tecnicos" in self.cleaned_data:
                project.tecnicos.set(self.cleaned_data["tecnicos"])
            if "familias" in self.cleaned_data:
                project.familias.set(self.cleaned_data["familias"])
        return project


# ---------------------------
# TECHNICIAN
# ---------------------------
class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
        fields = "__all__"
        labels = {
            "nome_tecnico": "Nome",
            "email": "E-mail",
            "telefone": "Telefone",
            "cpf": "CPF",
            "data_nascimento": "Data de Nascimento",
            "especialidade": "Especialidade",
        }
        widgets = {
            "nome_tecnico": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome completo"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@exemplo.com"}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(00) 00000-0000"}
            ),
            "cpf": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "000.000.000-00"}
            ),
            "data_nascimento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "especialidade": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        if cpf and not validate(cpf):
            raise forms.ValidationError("CPF inválido.")
        return re.sub(r"\D", "", cpf or "")


class TechnicianEditForm(TechnicianForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and getattr(self.instance, "cpf", None):
            cpf = self.instance.cpf
            if cpf and cpf.isdigit() and len(cpf) == 11:
                self.initial["cpf"] = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

# ---------------------------
# FAMILY
# ---------------------------
class FamilyForm(ModelForm):
    class Meta:
        model = Family
        exclude = ["terra", "subsistemas"]
        labels = {
            "nome_titular": "Nome do Titular",
            "data_inicio": "Data de Início",
            "contato": "Contato",
            "municipio": "Município",
            "projetos": "Projetos",
        }
        widgets = {
            "nome_titular": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do titular"}
            ),
            "data_inicio": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "contato": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Telefone ou e-mail"}
            ),
            "municipio": forms.Select(attrs={"class": "form-control"}),
            "projetos": forms.SelectMultiple(
                attrs={"class": "form-control", "size": 14}
            ),
        }


class FamilyEditForm(FamilyForm):

    def save(self, commit=True):
        family = super().save(commit=False)
        if commit:
            family.save()
            if "projetos" in self.cleaned_data:
                family.projetos.set(self.cleaned_data["projetos"])
        return family


# ---------------------------
# PRODUTO / FLUXO
# ---------------------------
class ProdutoForm(forms.Form):
    nome = forms.CharField(
        label="Nome do Produto",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    qtd = forms.FloatField(
        label="Quantidade",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    und = forms.CharField(
        label="Unidade de Medida",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    custo = forms.FloatField(
        label="Custo",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    valor = forms.FloatField(
        label="Valor Unitário",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    valor_potencial = forms.FloatField(
        label="Valor Potencial",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    destino = forms.CharField(
        label="Destino",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    descricao = forms.CharField(
        label="Descrição (Mundo Externo)",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
    )


ProdutoFormSet = formset_factory(ProdutoForm, extra=1)


class FluxoForm(forms.Form):
    nome_produto = forms.ChoiceField(
        choices=(),
        required=True,
        label="Produto",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    qtd = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Qtd",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    und = forms.CharField(
        required=False,
        label="Unidade de Medida",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    custo = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Custo",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    valor = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Valor Unitário",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    valor_potencial = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        label="Valor Potencial",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    destino = forms.ChoiceField(
        choices=(),
        required=False,
        label="Destino",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    DELETE = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


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


# ---------------------------
# SUBSYSTEM
# ---------------------------
class SubsystemForm(ModelForm):
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
        labels = {
            "nome_subsistema": "Nome do Subsistema",
            "descricao": "Descrição",
            "foto_subsistema": "Foto do Subsistema",
            "tipo": "Tipo",
        }
        widgets = {
            "nome_subsistema": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "foto_subsistema": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "tipo": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_foto_subsistema(self):
        foto = self.cleaned_data.get("foto_subsistema")
        if not foto:
            return foto
        extensoes_validas = [".jpg", ".jpeg", ".png"]
        ext = os.path.splitext(foto.name)[1].lower()
        if ext not in extensoes_validas:
            raise forms.ValidationError(
                "Envie uma imagem nos formatos JPG, JPEG ou PNG."
            )
        try:
            img = Image.open(foto)
            img.verify()
        except Exception:
            raise forms.ValidationError("O arquivo enviado não é uma imagem válida.")
        return foto

    def clean_produtos_base(self):
        data = self.cleaned_data.get("produtos_base", "")
        # aceita JSON lista ou linhas
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


class SubsystemEditForm(SubsystemForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, "produtos_base", None):
            pb = self.instance.produtos_base
            if isinstance(pb, list):
                linhas = []
                for item in pb:
                    nome = item.get("nome") if isinstance(item, dict) else str(item)
                    if nome:
                        linhas.append(nome)
                self.initial["produtos_base"] = "\n".join(linhas)
            elif isinstance(pb, str):
                self.initial["produtos_base"] = pb


# ---------------------------
# TIMELINE EVENT
# ---------------------------
class TimelineEventForm(ModelForm):
    class Meta:
        model = TimelineEvent
        exclude = ("family",)
        labels = {
            "titulo": "Título",
            "data": "Data",
            "descricao": "Descrição",
            "secao": "Seção",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "secao": forms.TextInput(attrs={"class": "form-control"}),
        }


class TimelineEventEditForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = [
            "titulo",
            "descricao",
            "data",
            "secao",
        ]

        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Título do evento",
                }
            ),
            "secao": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Seção do evento",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Descrição detalhada...",
                    "style": "resize: vertical;",
                }
            ),
            "data": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }
