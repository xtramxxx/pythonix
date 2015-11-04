#coding: utf-8
from django.shortcuts import render

def client_index(request):
    return render(request, 'app_client/index.html',)