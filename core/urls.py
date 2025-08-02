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
from seapac.views import index, register, flow, timeline, edit_family, list_families, calendar, family_profile, eventos_json, criar_evento, deletar_evento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('cadastrar/', register, name='register'),
    path('<str:id>/fluxo/', flow, name='flow'),
    path('<str:id>/timeline/', timeline, name='timeline'),
    path('editar-familia/<int:id>/', edit_family, name='edit_family'),
    path('lista-familias/', list_families, name='list_families'),
    path('calendario-visitas/', calendar, name='calendar'),
    path('<str:id>/perfil/', family_profile, name='family_profile'),
    path('api/events/', eventos_json),
    path('api/events/create/', criar_evento),
    path('api/events/delete/<int:event_id>/', deletar_evento),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)