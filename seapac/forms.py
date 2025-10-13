from django.forms import ModelForm
from django import forms
from .models import Family, Terrain, Project, Technician, Subsystem, TimelineEvent

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
        }
    
class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
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
            'municipio': forms.Select(attrs={'class': 'form-control'}),
            'comunidade': forms.TextInput(attrs={'class': 'form-control'}),
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
            'terra': forms.Select(attrs={'class': 'form-select'}),
            'projeto': forms.Select(attrs={'class': 'form-select'}),
        }

class SubsystemForm(ModelForm):
    class Meta:
        model = Subsystem
        fields = ['nome_subsistema', 'produtos_base']
        widgets = {
            'nome_subsistema': forms.TextInput(attrs={'class': 'form-control'}),
            'produtos_base': forms.Textarea(attrs={'class': 'form-select'})
        }

class TimelineEventForm(ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ['titulo', 'data', 'descricao', 'secao']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'secao': forms.TextInput(attrs={'class': 'form-control'}),
        }