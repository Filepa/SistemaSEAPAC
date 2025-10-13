from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'cpf', 'nome_cidade', 'endereco', 'nome_bairro', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF (apenas números)'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'nome_bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
        }

    #criando a senha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})


#formulário para login
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome de usuário' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Senha'}))

#formulário para edição do usuário (com adiçao de novas informações)
class PerfilForm(forms.ModelForm):
    """Formulário para editar perfil do usuário"""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'foto_perfil', 'nome_cidade',  'endereco', 'nome_bairro']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control'}),
            'nome_cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
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