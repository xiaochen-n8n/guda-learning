from django import forms
from django.forms.widgets import *
from .models import Host

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'cpu': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'mem': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
            'desc': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'可选项目'}),
        }