from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Urls de usuário
    path(
        "home/",
        TemplateView.as_view(template_name="homepage/principal.html"),
        name="home",
    ),
    path("cadastrar-user/", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("perfil/", views.perfil_view, name="perfil"),
    # Recuperação de senha
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.txt",
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Painel Adm
    path("gerenciar/", views.list_user, name="list_user"),
    path("gerenciar/criar/", views.criar_usuario_admin, name="criar_usuario_admin"),
    path(
        "gerenciar/editar/<int:pk>/",
        views.editar_usuario_admin,
        name="editar_usuario_admin",
    ),
    path("gerenciar/deletar/<int:pk>/", views.deletar_usuario, name="deletar_usuario"),
]
