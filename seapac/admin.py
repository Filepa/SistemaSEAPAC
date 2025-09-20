from django.contrib import admin
from django.utils.html import format_html
from .models import Family, Terrain, Project

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('nome_titular', 'data_inicio', 'contato', 'projeto', 'terra')

@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'comunidade')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('nome_projeto', 'descricao', 'data_inicio', 'data_fim', 'orcamento')