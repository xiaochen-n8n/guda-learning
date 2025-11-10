from django.shortcuts import render, HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def cmdb(request): #用于承载资产管理的核心功能。
    return HttpResponse("This is cmdb.")

def asset(request, asset_id):
    return HttpResponse("This is asset. asset_id: %s" % asset_id)
