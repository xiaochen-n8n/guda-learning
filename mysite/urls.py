from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from cmdb import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name='index'),
    path("add/", views.asset_add, name="asset_add"),
    path("edit/<int:pk>/", views.asset_edit, name="asset_edit"),
    path("delete/<int:pk>/", views.asset_delete, name="asset_delete"),
    path("collect/", views.collect, name="collect"),
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
