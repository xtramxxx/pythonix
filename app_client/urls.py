# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from app_client import views


urlpatterns = [
    url(r'^$', views.client_index, name='pythonix_client'),
]
