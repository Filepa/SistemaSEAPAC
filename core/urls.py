"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from seapac.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('cadastrar/', register, name='register'),
    path('<str:id>/fluxo/', flow, name='flow'),
    path('<str:family_id>/painel-subsistema/<str:subsystem_id>/', subsystem_panel, name='subsystem_panel'),
    path('<str:family_id>/editar-painel-subsistema/<str:subsystem_id>/', edit_subsystem_panel, name='edit_subsystem_panel'),
    path('<str:id>/timeline/', timeline, name='timeline'),
    path('<str:id>/editar-familia/', edit_family, name='edit_family'),
    path('lista-familias/', list_families, name='list_families'),
    path('lista-projetos/', list_projects, name='list_projects'),
    path('lista-projetos/novo/', create_projects, name='create_projects'),
    path('lista-projetos/detalhar/<int:pk>/', detail_projects, name='detail_projects'),
    path('lista-projetos/editar/<int:pk>/', edit_projects, name='edit_projects'),
    path('lista-projetos/deletar/<int:pk>/', delete_projects, name='delete_projects'),
    path('lista-tecnicos/', list_tecs, name='list_tecs'),
    path('lista-tecnicos/novo/', create_tecs, name='create_tecs'),
    path('lista-tecnicos/detalhar/<int:pk>/', detail_tecs, name='detail_tecs'),
    path('lista-tecnicos/editar/<int:pk>/', edit_tecs, name='edit_tecs'),
    path('lista-tecnicos/deletar/<int:pk>/', delete_tecs, name='delete_tecs'),
    path('calendario-visitas/', calendar, name='calendar'),
    path('<str:id>/editar-fluxo/', edit_flow, name='edit_flow'),
    path('<str:id>/perfil-familia/', family_profile, name='family_profile'),
    path('api/events/', eventos_json),
    path('api/events/create/', criar_evento),
    path('api/events/delete/<int:event_id>/', deletar_evento),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)