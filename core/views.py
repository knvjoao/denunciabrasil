from .models import Denuncia
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CriarUsuarioForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse


#Página inicial. Quando o usuário é redirecionado a home ao fazer uma denúncia, é criado o valor denuncia_token, para passar ao usuário.
def home(request, denuncia_token=None):
    denuncia_token = request.GET.get('denuncia_token')
    if denuncia_token:
        contexto = {'denuncia_token': denuncia_token}
    else:
        contexto = {}

    return render(request, 'core/home.html', contexto)         #O dicionário contexto é criado para poder ser passado ao html e usado numa condicional que pode mostrar o token.


#Cadastro de usuário.
def cadastrar(request):
    if request.method == 'POST':
        form = CriarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect('home')
        else:
            messages.error(request, "Erro ao criar a conta. Verifique se digitou o email corretamente. Sua senha deve conter letras e números, mais de 7 dígitos e não pode conter o nome de usuário.")
            return render(request, 'core/cadastrar.html', {'form': form})
    else:
        form = CriarUsuarioForm()

    return render(request, 'core/cadastrar.html', {'form': form})


#Entrar/login.
def entrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)        
        if user is not None:
            login(request, user)
            return redirect('minhas_denuncias')
        else:
            return render(request, 'core/entrar.html', {'error': 'Usuário não encontado ou senha errada. Verifique os caracteres inseridos.'})
            
    return render(request, 'core/entrar.html')

#Sair/logout.
def sair(request):
    logout(request)

    return redirect('home')


#Denunciar como usuário. Uso da senha, para aumentar a segurança.
@login_required
def nova_denuncia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        senha = request.POST.get('senha')
        denuncia = Denuncia.objects.create(usuario=request.user, titulo=titulo, descricao=descricao, senha=senha)
        #Passa para home o token da denúncia:
        return redirect(f"{reverse('home')}?denuncia_token={denuncia.token}")
    
    return render(request, 'core/nova_denuncia.html')


#Denúncias feitas pelo usuário.
@login_required
def minhas_denuncias(request):
    denuncias = Denuncia.objects.filter(usuario=request.user)

    return render(request, 'core/minhas_denuncias.html', {'denuncias': denuncias})


#Ver denúncia. Precisa de token e senha.
def ver_denuncia(request, token):
    denuncia = get_object_or_404(Denuncia, token=token)
    if request.method == 'POST':
        #Ao criar a denúncia, o usuário define denuncia.senha, que deve ser igual à informada para visualizá-la.
        senha_informada = request.POST.get('senha')
        if senha_informada == denuncia.senha:
            return render(request, 'core/ver_denuncia.html', {'denuncia': denuncia, 'senha_valida': True})
        else:
            return render(request, 'core/ver_denuncia.html', {'denuncia': denuncia, 'senha_valida': False})

    return render(request, 'core/ver_denuncia.html', {'denuncia': denuncia})


#Realizar denúncia anônima. Toda denúncia deve estar associada a um usuário, mesmo se for definido como None.
def denuncia_anonima(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        senha = request.POST.get('senha')
        denuncia = Denuncia.objects.create(usuario=None, titulo=titulo, descricao=descricao, senha=senha)
        return redirect(f"{reverse('home')}?denuncia_token={denuncia.token}")
    
    return render(request, 'core/denuncia_anonima.html')