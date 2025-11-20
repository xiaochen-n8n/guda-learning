from django.contrib import admin
from django.urls import path
from cmdb import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("add/", views.asset_add, name="asset_add"),
    path("edit/<int:pk>/", views.asset_edit, name="asset_edit"),
    path("delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("collect/", views.collect, name="collect"),
]
