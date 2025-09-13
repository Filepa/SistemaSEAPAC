from django.forms import ModelForm
from django import forms
from .models import Family, Subsystem, Terrain, Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'nome_projeto': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            #'tecnicos': forms.Textarea(attrs={'class': 'form-control'}), #vai virar um select ainda
            #'familias': forms.Select(attrs={'class': 'form-select'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
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

class FluxoForm(forms.Form):
    nome_produto = forms.CharField(widget=forms.HiddenInput())
    porcentagem = forms.DecimalField(required=False, max_digits=6, decimal_places=2)
    destino = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

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