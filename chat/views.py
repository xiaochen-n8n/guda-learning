from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile

def index(request):
    nickname = None
    if request.user.is_authenticated:
        try:
            nickname = Profile.objects.get(user=request.user).nickname
        except Profile.DoesNotExist:
            nickname = request.user.username
    return render(request, 'index.html', {'nickname': nickname})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        if username and password and nickname and not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user, nickname=nickname)
            login(request, user)
            return redirect('index')
        return render(request, 'index.html', {'error': '注册失败'})
    return redirect('index')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if nickname:
                Profile.objects.update_or_create(user=user, defaults={'nickname': nickname})
            login(request, user)
            return redirect('index')
        return render(request, 'index.html', {'error': '登录失败'})
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')
