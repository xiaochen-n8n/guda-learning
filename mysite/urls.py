from django.contrib import admin
from django.urls import path
from cmdb import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("cmdb/", views.cmdb),
    path("cmdb/asset/<int:asset_id>/", views.asset),
]
