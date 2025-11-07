from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='homepage/principal.html'), name='home'),
    path('cadastrar-user/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
]