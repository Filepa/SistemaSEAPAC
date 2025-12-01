from django.contrib import admin
from .models import (
    Technician,
    Municipality,
    Family,
    Subsystem,
    FamilySubsystem,
    Project,
    TimelineEvent,
    Evento,
)

# ---------------------------
# Inline para relações
# ---------------------------


class FamilySubsystemInline(admin.TabularInline):
    model = FamilySubsystem
    extra = 1
    autocomplete_fields = ["subsystem"]
    verbose_name = "Subsistema da Família"
    verbose_name_plural = "Subsistemas da Família"
    show_change_link = True


class FamilyInline(admin.TabularInline):
    model = Project.familias.through
    extra = 1
    verbose_name = "Família no Projeto"
    verbose_name_plural = "Famílias no Projeto"


class TechnicianInline(admin.TabularInline):
    model = Project.tecnicos.through
    extra = 1
    verbose_name = "Técnico no Projeto"
    verbose_name_plural = "Técnicos no Projeto"


# ---------------------------
# MODELOS PRINCIPAIS
# ---------------------------


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ("nome_tecnico", "telefone", "email", "cpf")
    search_fields = ("nome_tecnico", "cpf", "email")
    list_per_page = 10
    ordering = ["nome_tecnico"]


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Subsystem)
class SubsystemAdmin(admin.ModelAdmin):
    list_display = ("nome_subsistema", "tipo", "descricao_resumida", "has_valid_photo")
    list_filter = ("tipo",)
    search_fields = ("nome_subsistema",)
    readonly_fields = ("foto_preview",)

    def descricao_resumida(self, obj):
        return (
            (obj.descricao[:60] + "...") if len(obj.descricao) > 60 else obj.descricao
        )

    descricao_resumida.short_description = "Descrição"

    def foto_preview(self, obj):
        if obj.get_photo_url():
            return f'<img src="{obj.get_photo_url()}" width="120" style="border-radius: 6px;" />'
        return "(Sem foto)"

    foto_preview.allow_tags = True
    foto_preview.short_description = "Prévia da Imagem"


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        "nome_titular",
        "municipio",
        "get_projetos",
        "get_nivel",
        "get_pontuacao",
    )
    list_filter = ("municipio", "projetos")
    search_fields = ("nome_titular", "municipio__nome")
    inlines = [FamilySubsystemInline]
    list_select_related = ("municipio",)
    ordering = ["nome_titular"]
    list_per_page = 10

    def get_projetos(self, obj):
        return ", ".join([p.nome_projeto for p in obj.projetos.all()])

    get_projetos.short_description = "Projetos"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("nome_projeto", "status", "data_inicio", "data_fim", "orcamento")
    list_filter = ("status", "data_inicio")
    search_fields = ("nome_projeto", "descricao")
    inlines = [FamilyInline, TechnicianInline]
    list_per_page = 10
    fieldsets = (
        ("Informações Gerais", {"fields": ("nome_projeto", "descricao", "status")}),
        ("Datas e Orçamento", {"fields": (("data_inicio", "data_fim"), "orcamento")}),
    )


@admin.register(FamilySubsystem)
class FamilySubsystemAdmin(admin.ModelAdmin):
    list_display = ("family", "subsystem", "produtos_saida_count")
    search_fields = ("family__nome_titular", "subsystem__nome_subsistema")
    list_select_related = ("family", "subsystem")

    def produtos_saida_count(self, obj):
        return len(obj.produtos_saida or [])

    produtos_saida_count.short_description = "Nº de produtos"


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("titulo", "family", "data", "secao")
    list_filter = ("data",)
    search_fields = ("titulo", "descricao", "family__nome_titular")
    date_hierarchy = "data"
    list_select_related = ("family",)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "familia", "data", "confirmado")
    list_filter = ("confirmado",)
    search_fields = ("titulo", "familia__nome_titular")
    date_hierarchy = "data"
    list_select_related = ("familia",)
