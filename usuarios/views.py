from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UsuarioCreationForm,
    LoginForm,
    PerfilForm,
    UsuarioFiltroForm,
    UsuarioEditForm,
)
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404


def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            grupo_tecnico, created = Group.objects.get_or_create(name="TECNICOS")
            user.groups.add(grupo_tecnico)

            messages.success(
                request, "Cadastro realizado com sucesso! Faça login para continuar."
            )
            return redirect("login")
    else:
        form = UsuarioCreationForm()

    return render(request, "login/cadastrar.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Bem-vindo ao Sistema SEAPAC, {user.username}!"
                )

                next_page = request.GET.get("next", "dashboard")
                return redirect(next_page)

        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = LoginForm()

    return render(request, "login/login.html", {"form": form})



@require_POST
def logout_view(request):
    request.session.flush()
    messages.info(request, "Você saiu do sistema.")
    return redirect("index")


@never_cache
@login_required
def perfil_view(request):
    user = request.user
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("perfil")
    else:
        form = PerfilForm(instance=request.user)

    return render(request, "login/perfil.html", {"form": form, "user": user})


def index(request):
    return render(request, "homepage/index.html")


@never_cache
@login_required
def list_user(request):
    if not request.user.is_administrador and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("dashboard")

    usuarios = Usuario.objects.all().order_by("-date_joined")

    filtro_form = UsuarioFiltroForm(request.GET or None)

    if filtro_form.is_valid():

        username = filtro_form.cleaned_data.get("username")
        if username:
            usuarios = usuarios.filter(username__icontains=username)

        email = filtro_form.cleaned_data.get("email")
        if email:
            usuarios = usuarios.filter(email__icontains=email)

        cpf = filtro_form.cleaned_data.get("cpf")
        if cpf:
            usuarios = usuarios.filter(cpf__icontains=cpf)

        nome_cidade = filtro_form.cleaned_data.get("cidade")
        if nome_cidade:
            usuarios = usuarios.filter(nome_cidade__icontains=nome_cidade)

        grupo = filtro_form.cleaned_data.get("grupo")
        if grupo:
            usuarios = usuarios.filter(groups=grupo)

        is_active = filtro_form.cleaned_data.get("is_active")
        if is_active == "true":
            usuarios = usuarios.filter(is_active=True)
        elif is_active == "false":
            usuarios = usuarios.filter(is_active=False)

    itens_por_pagina = 10
    paginator = Paginator(usuarios, itens_por_pagina)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    return render(
        request,
        "painel/list_user.html",
        {
            "usuarios": page_obj,
            "page_obj": page_obj,
            "filtro_form": filtro_form,
        },
    )


@login_required
def criar_usuario_admin(request):

    if not request.user.is_administrador and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("dashboard")

    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            grupo_simples, created = Group.objects.get_or_create(name="TECNICOS")
            user.groups.add(grupo_simples)

            messages.success(request, f"Usuário {user.username} criado com sucesso!")
            return redirect("list_user")
    else:
        form = UsuarioCreationForm()

    return render(
        request, "painel/form_user.html", {"form": form, "titulo": "Criar Novo Usuário"}
    )


@login_required
def editar_usuario_admin(request, pk):

    if not request.user.is_administrador and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("list_user")

    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Usuário {usuario.username} atualizado com sucesso!"
            )
            return redirect("list_user")
    else:
        form = UsuarioEditForm(instance=usuario)

    return render(
        request,
        "painel/form_user.html",
        {
            "form": form,
            "titulo": f"Editar Usuário: {usuario.username}",
            "usuario": usuario,
            "tipo": "edit",
        },
    )


@login_required
def deletar_usuario(request, pk):

    if not request.user.is_administrador and not request.user.is_superuser:
        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("list_user")

    usuario = get_object_or_404(Usuario, pk=pk)

    if usuario == request.user:
        messages.error(request, "Você não pode deletar seu próprio usuário!")
        return redirect("list_user")

    if usuario.is_superuser:
        messages.error(request, "Não é possível deletar um superusuário!")
        return redirect("list_user")

    if request.method == "POST":
        username = usuario.username
        usuario.delete()
        messages.success(request, f"Usuário {username} deletado com sucesso!")
        return redirect("list_user")

    return render(request, "painel/confirmar_delete_usuario.html", {"usuario": usuario})
