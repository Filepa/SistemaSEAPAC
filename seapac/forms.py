from django.forms import ModelForm
from django import forms
from .models import Family, Subsystem, Terrain, Project, Tecnicos

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = { #falta aprimorar o select de técnicos, famílias e municípios (n sei como fzr o multiselect, estou vendo)
            'nome_projeto': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'stle': 'max-width:400px;'}),
            'tecnicos': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}), 
            'familias': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'orcamento': forms.Textarea(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }

    
class TecnicosForm(ModelForm):
    class Meta:
        model = Tecnicos
        fields = [
            "nome_tecnico",
            "descricao",
            "email",
            "telefone",
            "cpf",
            "data_nascimento",
        ]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3, "placeholder": "Descreva a experiência e área de atuação do técnico..."})
            #"foto": forms.FileInput(attrs={'class': 'form-control-file'}),
        }
class TerrainForm(ModelForm):
    class Meta:
        model = Terrain
        fields = '__all__'
        widgets = {
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'comunidade': forms.TextInput(attrs={'class': 'form-control'}),
            'tamanho_m2': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SubsystemForm(ModelForm):

    class Meta:
        model = Subsystem
        fields = '__all__'
        widgets = {
            'nome_subsistema': forms.TextInput(attrs={'class': 'form-control'}),
            'produtos_entrada': forms.Select(attrs={'class': 'form-select'}),
            'produtos_saida': forms.Select(attrs={'class': 'form-select'}),
            'destino_produtos_entrada': forms.Select(attrs={'class': 'form-select'}),
            'destino_produtos_saida': forms.Select(attrs={'class': 'form-select'}),
            'foto_subsistema': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class FamilyForm(ModelForm):

    class Meta:
        model = Family
        exclude = ['terra']
        fields = '__all__'
        widgets = {
            'nome_titular': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_conjuge': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'bpc': forms.TextInput(attrs={'class': 'form-control'}),
            'nis': forms.TextInput(attrs={'class': 'form-control'}),
            'dap': forms.TextInput(attrs={'class': 'form-control'}),
            'aposentadoria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'auxilio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'escolaridade': forms.Select(attrs={'class': 'form-select'}),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'terra': forms.Select(attrs={'class': 'form-select'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
            'subsistemas': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }