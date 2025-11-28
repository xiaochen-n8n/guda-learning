from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Host
from .forms import HostForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def index(request):
    host_list = Host.objects.all()
    return render(request, "main.html", {"host_list": host_list})

@login_required
def asset_add(request):
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else: # GET方法
        form = HostForm()
    return render(request, "add.html", {"form": form})

@login_required
def asset_edit(request, pk: int):
    host = get_object_or_404(Host, pk=pk)
    if request.method == "POST":
        form = HostForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = HostForm(instance=host)
    return render(request, "edit.html", {"form": form, "host": host})

@login_required
def asset_delete(request, pk):
    from django.shortcuts import get_object_or_404, redirect
    host = get_object_or_404(Host, pk=pk)
    host.delete()
    return redirect('index')

@csrf_exempt
def collect(request):
    """
    资产收集接口
    :param request:
    字典格式为：
    {
        "hostname": "host1",
        "ip": "192.168.1.1",
        "cpu": "Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz",
        "mem": "128GB",
        "disk": "1TB",
        "desc": "测试资产"
    }
    :return:
    """
    asset_info = json.loads(request.body)
    if request.method == 'POST':
        hostname = asset_info.get('hostname')
        ip = asset_info.get('ip')
        cpu = asset_info.get('cpu')
        mem = asset_info.get('mem')
        disk = asset_info.get('disk')
        desc = asset_info.get('desc')
        try:
            host = Host.objects.get(hostname=hostname)
        except Host.DoesNotExist:
            host = Host()
        host.hostname = hostname
        host.ip = ip
        host.cpu = cpu
        host.mem = mem
        host.disk = disk
        host.desc = desc
        host.save()
    return HttpResponse("success")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {"error": "用户名或密码错误"})
    return render(request, "login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "用户名已存在"})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "register.html")


def user_logout(request):
    logout(request)
    return redirect("login")