from django.forms import ModelForm
from django import forms
from .models import Family, Project, Technician, Subsystem, TimelineEvent
from django.forms import formset_factory
import json

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'nome_projeto': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'stle': 'max-width:400px;'}),
            'tecnicos': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}), 
            'familias': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'orcamento': forms.Textarea(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
        fields = '__all__'
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3, "placeholder": "Descreva a experiência e área de atuação do técnico...",'class': 'form-control'}),
            "nome_tecnico": forms.TextInput(attrs={'class': 'form-control'}),
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "telefone": forms.TextInput(attrs={'class': 'form-control'}),
            "cpf": forms.TextInput(attrs={'class': 'form-control'}),
            "data_nascimento": forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            #"foto": forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
class FamilyForm(ModelForm):
    class Meta:
        model = Family
        exclude = ['terra', 'subsistemas']
        fields = '__all__'
        widgets = {
            'nome_titular': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-select'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
        }

class ProdutoForm(forms.Form):
    nome = forms.CharField(label="Nome do Produto", required=True)
    qtd = forms.FloatField(label="Quantidade", required=False)
    custo = forms.FloatField(label="Custo", required=False)
    valor = forms.FloatField(label="Valor", required=False)
    destino = forms.CharField(label="Destino", required=False)
    porcentagem = forms.FloatField(label="Porcentagem", required=False)

ProdutoFormSet = formset_factory(ProdutoForm, extra=1)

class SubsystemForm(forms.ModelForm):
    produtos_base = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite um produto por linha:\nCarne\nLeite\nEsterco',
                'rows': 5
            }
        ),
        label='Produtos Base'
    )

    class Meta:
        model = Subsystem
        fields = ['nome_subsistema', 'descricao', 'produtos_base', 'foto_subsistema', 'tipo']
        widgets = {
            'nome_subsistema': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'foto_subsistema': forms.FileInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_produtos_base(self):
        data = self.cleaned_data.get('produtos_base', '')

        if isinstance(data, str) and data.strip().startswith('['):
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                raise forms.ValidationError("JSON inválido. Use uma lista ou uma linha por produto.")

        linhas = [linha.strip() for linha in str(data).splitlines() if linha.strip()]
        produtos = [{"nome": linha, "fluxos": []} for linha in linhas]

        return produtos

class TimelineEventForm(ModelForm):
    class Meta:
        model = TimelineEvent
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'secao': forms.TextInput(attrs={'class': 'form-control'}),
        }