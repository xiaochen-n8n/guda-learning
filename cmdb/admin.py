from django.contrib import admin
from .models import Host
# Register your models here.

class HostAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'ip', 'cpu', 'mem', 'disk', 'desc']
admin.site.register(Host, HostAdmin)