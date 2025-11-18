from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from seapac.models import Municipality
from .validators import validate
import re
from PIL import Image

#Criando um usuário:
class UsuarioCreationForm(UserCreationForm):
    nome_cidade = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione sua cidade",
        label="Cidade"
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'cpf', 'nome_cidade', 'endereco', 'nome_bairro', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

    #validando CPF
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']

        if not validate(cpf):
            raise forms.ValidationError("CPF inválido.")

        return re.sub(r'\D', '', cpf)


#formulário para login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome de usuário' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Senha'}))

#formulário para edição do usuário (com adiçao de novas informações)
class PerfilForm(forms.ModelForm):
    nome_cidade = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione sua cidade",
        label="Cidade"
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto_perfil', 'nome_cidade', 'endereco', 'nome_bairro']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }
        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'foto_perfil': 'Foto de Perfil',
            'nome_cidade': 'Cidade',
            'endereco': 'Endereço',
            'nome_bairro': 'Bairro',
        }

    #Função para validar o tipo de imagem enviada pelo usuário
    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')

        # Caso o usuário não envie nada (edição sem trocar a foto), retorna normal
        if not foto:
            return foto

        # Verificar a extensão permitida
        extensoes_validas = ['.jpg', '.jpeg', '.png']
        import os
        ext = os.path.splitext(foto.name)[1].lower()
        if ext not in extensoes_validas:
            raise forms.ValidationError("Envie uma imagem nos formatos JPG, JPEG ou PNG.")

        # Verificar se o arquivo é realmente uma imagem
        try:
            img = Image.open(foto)
            img.verify()  # verifica estrutura interna

        except Exception:
            raise forms.ValidationError("O arquivo enviado não é uma imagem válida.")

        return foto