from django.shortcuts import render, HttpResponse, redirect
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