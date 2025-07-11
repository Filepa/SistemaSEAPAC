from django.contrib import admin
from .models import User, Family

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contato')
    fields = ('nome', 'email', 'contato')

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('nome_familia', 'nome_titular', 'nome_conjuge', 'data_nasc', 'data_inic', 'cpf', 'contato',  'bpc', 'nis', 'dap', 'aposentadoria', 'auxilio', 'escolaridade')
    fields = ('nome_familia', 'nome_titular', 'nome_conjuge', 'data_nasc', 'contato',  'bpc', 'nis', 'dap', 'aposentadoria', 'auxilio', 'escolaridade')
