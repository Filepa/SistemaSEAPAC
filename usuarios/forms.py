from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from django.contrib.auth.models import Group
from seapac.models import Municipality
from .validators import validate
import re
from PIL import Image


# Criando um usuário:
class UsuarioCreationForm(UserCreationForm):
    nome_cidade = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Selecione sua cidade",
        label="Cidade",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "cpf",
            "nome_cidade",
            "endereco",
            "nome_bairro",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome de usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "seu@email.com"}
            ),
            "cpf": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite seu CPF"}
            ),
            "endereco": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Endereço completo"}
            ),
            "nome_bairro": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Bairro"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Senha"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirme a senha"}
        )

    # validando CPF
    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]

        if not validate(cpf):
            raise forms.ValidationError("CPF inválido.")

        return re.sub(r"\D", "", cpf)


# formulário para login
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nome de usuário"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Senha"}
        )
    )


# formulário para edição do usuário (com adiçao de novas informações)
class PerfilForm(forms.ModelForm):
    nome_cidade = forms.ModelChoiceField(
        queryset=Municipality.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Selecione sua cidade",
        label="Cidade",
    )

    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "email",
            "foto_perfil",
            "nome_cidade",
            "endereco",
            "nome_bairro",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Primeiro nome"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Sobrenome"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "seu@email.com"}
            ),
            "foto_perfil": forms.FileInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Endereço completo"}
            ),
            "nome_bairro": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Bairro"}
            ),
        }
        labels = {
            "first_name": "Primeiro Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "foto_perfil": "Foto de Perfil",
            "nome_cidade": "Cidade",
            "endereco": "Endereço",
            "nome_bairro": "Bairro",
        }

    # Função para validar o tipo de imagem enviada pelo usuário
    def clean_foto_perfil(self):
        foto = self.cleaned_data.get("foto_perfil")

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


# filtro de usuários
class UsuarioFiltroForm(forms.Form):

    username = forms.CharField(
        required=False,
        label="Nome de Usuário",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por username..."}
        ),
    )

    email = forms.EmailField(
        required=False,
        label="E-mail",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Buscar por e-mail..."}
        ),
    )

    cpf = forms.CharField(
        required=False,
        label="CPF",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por CPF..."}
        ),
    )

    nome_cidade = forms.CharField(
        required=False,
        label="Cidade",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar por cidade..."}
        ),
    )

    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Grupo",
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="Todos os grupos",
    )

    is_active = forms.ChoiceField(
        required=False,
        label="Status",
        choices=[("", "Todos"), ("true", "Ativo"), ("false", "Inativo")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )


# Editar usuário no painel
class UsuarioEditForm(forms.ModelForm):

    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Grupos",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "cpf",
            "nome_cidade",
            "endereco",
            "nome_bairro",
            "foto_perfil",
            "is_active",
            "is_staff",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cpf": forms.TextInput(attrs={"class": "form-control"}),
            "nome_cidade": forms.TextInput(attrs={"class": "form-control"}),
            "endereco": forms.TextInput(attrs={"class": "form-control"}),
            "nome_bairro": forms.TextInput(attrs={"class": "form-control"}),
            "foto_perfil": forms.FileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "username": "Nome de Usuário",
            "first_name": "Primeiro Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "cpf": "CPF",
            "nome_cidade": "Cidade",
            "endereco": "Endereço",
            "nome_bairro": "Bairro",
            "foto_perfil": "Foto de Perfil",
            "is_active": "Usuário Ativo",
            "is_staff": "Acesso ao Admin",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["grupos"].initial = self.instance.groups.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Atualizar grupos
            if "grupos" in self.cleaned_data:
                user.groups.set(self.cleaned_data["grupos"])
        return user

        # Função para validar o tipo de imagem enviada pelo usuário

    def clean_foto_perfil(self):
        foto = self.cleaned_data.get("foto_perfil")

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

        # validando CPF

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]

        if not validate(cpf):
            raise forms.ValidationError("CPF inválido.")

        return re.sub(r"\D", "", cpf)
