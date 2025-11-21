from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ["username", "email", "cpf", "nome_cidade", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "groups"]
    search_fields = ["username", "email", "cpf"]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações adicionais",
            {
                "fields": (
                    "cpf",
                    "nome_cidade",
                    "endereco",
                    "nome_bairro",
                    "foto_perfil",
                ),
            },
        ),
    )
