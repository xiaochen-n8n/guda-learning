from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Host
from .forms import HostForm
# Create your views here.
def index(request):
    host_list = Host.objects.all()
    return render(request, "main.html", {"host_list": host_list})

def asset_add(request):
    if request.method == "POST":
        form = HostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else: # GET方法
        form = HostForm()
    return render(request, "add.html", {"form": form})

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

# @require_POST
# def asset_delete(request, pk):
#     host = get_object_or_404(Host, pk=pk)
#     host.delete()
#     return redirect('index')

# @require_POST
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