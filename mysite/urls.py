from django.contrib import admin
from django.urls import path
from cmdb import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("add/", views.asset_add, name="asset_add"),
]
