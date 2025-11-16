from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UsuarioCreationForm, LoginForm,PerfilForm
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group

#view para novos usuários:
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Adicionar usuário ao grupo TECNICOS por padrão
            grupo_tecnico, created = Group.objects.get_or_create(name='TECNICOS')
            user.groups.add(grupo_tecnico)
            
            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = UsuarioCreationForm()
    
    return render(request, 'login/cadastrar.html', {'form': form})

#view para login:
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo ao Sistema SEAPAC, {user.username}!')
                
                # Redireciona para a página principal
                next_page = request.GET.get('next','dashboard')
                return redirect(next_page)

        #quando o login não confere com os dados cadastrados:        
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'login/login.html', {'form': form})

#view para sair da aplicação (ou seja, logout):

@require_POST
def logout_view(request):
    request.session.flush()  # encerra a sessão com seguranç
    messages.info(request, 'Você saiu do sistema.')
    return redirect('index')
    

#view para visualizar o perfil do usuário:
@never_cache
@login_required
def perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    
    return render(request, 'login/perfil.html', {'form': form, 'user': user})

def index(request):
    return render(request, 'homepage/index.html')