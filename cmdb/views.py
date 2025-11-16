from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
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

def asset_delete(request, pk):
    from django.shortcuts import get_object_or_404, redirect
    host = get_object_or_404(Host, pk=pk)
    host.delete()
    return redirect('index')