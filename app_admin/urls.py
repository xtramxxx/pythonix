# coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin
from app_admin import views


urlpatterns = [
    url(r'^$', views.AdminIndexPage.as_view(), name='pythonix_admin'),
    url(r'^create_client/$', views.CreateClient.as_view(), name='create_client'),
    url(r'^client_info/(?P<pk>\d+)/$', views.ClientInfoView.as_view(), name='client_info'),
    url(r'^clients_list/(?P<pk>\d+)/$', views.ClientsList.as_view(), name='clients_list'),
    url(r'^del_client/(?P<pk>\d+)/$', views.ClientDelete.as_view(), name='del_client'),

    url(r'^get_free_ipaddress/(\d{1,9})/$', views.get_free_ipaddress, name='get_free_ipaddress'),
    url(r'^get_client_groups/(\d{1,9})/$', views.get_client_groups, name='get_client_groups'),
    url(r'^abbreviation_physical_network/(\d{1,9})/$', views.abbreviation_physical_network, name='abbreviation_physical_network'),
    url(r'^update_password/(\d{1,9})/$', views.update_password, name='update_password'),
    url(r'^pay_balance/(\d{1,9})/(\d{1,9})/$', views.pay_balance, name='pay_balance'),
    url(r'^client_on_off/(\d{1,9})/(\d{1,9})/$', views.client_on_off, name='client_on_off'),
    url(r'^send_sms_info_client_ajax/(\d{1,9})/(\d{1,9})/$', views.sendSmsInfoClientAjax, name='send_sms_info_client_ajax'),
    url(r'^get_status_client/(\d{1,9})/$', views.getStatusClient, name='get_status_client'),
    url(r'^report_pay_admin_list/$', views.ReportPayAdminList.as_view(), name='report_pay_admin_list'),
]
