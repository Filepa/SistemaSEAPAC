from django.forms import ModelForm
from django import forms
from .models import Family

class FamilyForm(ModelForm):

    class Meta:
        model = Family
        fields = '__all__'
        widgets = {
            'nome_titular' : forms.TextInput(attrs={'class': 'form-control' }),
            'cpf' : forms.TextInput(attrs={'class': 'form-control' }),
            'data_nasc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'data_inic': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'contato': forms.TextInput(attrs={'class': 'form-control',}),
            'bpc': forms.TextInput(attrs={'class': 'form-control'}),
            'nis': forms.TextInput(attrs={'class': 'form-control'}),
            'dap': forms.TextInput(attrs={'class': 'form-control'}),
            'aposentadoria': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'auxilio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'escolaridade': forms.Select(attrs={'class': 'form-select'}),
        }