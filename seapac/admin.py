from django.contrib import admin
from django.utils.html import format_html
from .models import User, Family, Terrain, Project, Subsystem, Tecnicos

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contato', 'foto_perfil')

    def foto_perfil(self, obj):
        if obj.foto_perfil:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.foto_perfil.url
            )
        return "Sem foto"
    foto_perfil.short_description = 'Foto de Perfil'

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('nome_titular', 'nome_conjuge', 'data_nascimento', 'data_inicio', 'cpf', 'contato', 'bpc', 'nis', 'dap', 'aposentadoria', 'auxilio', 'escolaridade', 'projeto', 'terra')

@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'latitude', 'longitude', 'comunidade', 'tamanho_m2')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nome_projeto', 'descricao', 'data_inicio', 'data_fim', 'orcamento')

@admin.register(Tecnicos)
class TecnicostAdmin(admin.ModelAdmin):
    list_display = ('nome_tecnico', 'descricao', 'telefone', 'cpf', 'email', 'data_nascimento') #'foto',

#@admin.register(Subsystem)
#class SubsystemAdmin(admin.ModelAdmin):
#    list_display = ('nome_subsistema', 'foto_subsistema', 'produtos_entrada', 'produtos_saida', 'destino_produtos_entrada', 'destino_produtos_saida', 'produtos_entrada_opcoes', 'produtos_saida_opcoes')
#
#    def foto_subsistema(self, obj):
#        if obj.foto_subsistema:
#            return format_html(
#                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
#                obj.foto_subsistema.url
#            )
#        return "Sem foto"
#    foto_subsistema.short_description = 'Foto do Subsistema'