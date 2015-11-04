#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import get_hasher
from django.utils.crypto import get_random_string
from django.http import JsonResponse

from hashlib import sha1
import json
import iplib

import app_admin.models as app_admin_models
import app_core.admin_mixin as admin_mixin
import forms

# Scripts MikroTik
import app_scripts.client_in_mikrotik
import app_scripts.update_client_info_mikrotik
import app_scripts.client_on_off
import app_scripts.client_status
import app_scripts.client_delete

import app_scripts.send_sms.smsc_api as smsc


def make_password(password, salt=None, hasher='default'):
    UNUSABLE_PASSWORD_PREFIX = '!'
    UNUSABLE_PASSWORD_SUFFIX_LENGTH = 40

    if password is None:
        return UNUSABLE_PASSWORD_PREFIX + get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH)
    hasher = get_hasher(hasher)

    if not salt:
        salt = hasher.salt()

    return password, hasher.encode(password, salt)


def admin_index(request):
    return render(request, 'app_admin/index.html',)


class AdminIndexPage(admin_mixin.BaseAdminContentMixin, ListView):
    model = app_admin_models.Clients
    template_name = 'app_admin/index.html'

    def get_context_data(self, **kwargs):
        context = super(AdminIndexPage, self).get_context_data(**kwargs)
        return context


class CreateClient(admin_mixin.BaseAdminContentMixin, CreateView):
    model = app_admin_models.Clients
    fields = ['first_name', 'last_name', 'email', 'username', 'ip_address', 'ipv6_address', 'send_sms', 'select_tarif',
              'select_clients_group', 'select_street', 'mobile_phone',
                'home_address', 'balance']
    template_name = 'app_admin/create_client.html'
    success_url = 'pythonix_admin:pythonix_admin'


    def get_success_url(self):
        self.success_url = reverse(self.success_url)
        return super(CreateClient, self).get_success_url()

    def get_context_data(self, **kwargs):
        context = super(CreateClient, self).get_context_data(**kwargs)
        context['physical_networks'] = app_admin_models.PhysicalNetwork.objects.all()
        return context


    def form_valid(self, form):
        password, enctipt_password = make_password(password=get_random_string(9, '1234567890'),
                                  salt=None,
                                  hasher='unsalted_md5')

        user_object = app_admin_models.Clients.objects.create_user(username=form.cleaned_data['username'],password=password,
            email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
            ip_address=form.cleaned_data['ip_address'], ipv6_address=form.cleaned_data['ipv6_address'], send_sms=form.cleaned_data['send_sms'],
            select_tarif=form.cleaned_data['select_tarif'], select_clients_group=form.cleaned_data['select_clients_group'],
            select_street=form.cleaned_data['select_street'], mobile_phone=form.cleaned_data['mobile_phone'],
            home_address=form.cleaned_data['home_address'], balance=form.cleaned_data['balance'], key=password)
        user_object.is_staff = True

        try:
            for server in app_admin_models.Servers.objects.filter(physical_network=user_object.select_clients_group.select_server.physical_network):
                app_scripts.client_in_mikrotik.addClient(server.network_address, server.api_port, server.login, server.password,
                    user_object.username, password, user_object.ip_address, "", user_object.select_tarif.speed_up, user_object.select_tarif.speed_up_unit,
                    user_object.select_tarif.speed_down, user_object.select_tarif.speed_down_unit)
        except:
            pass
        else:
            user_object.save()

        return HttpResponseRedirect("/pythonix_admin/client_info/"+str(user_object.id))


# Отображение списка клиентов группы
class ClientsList(admin_mixin.BaseAdminContentMixin, ListView):

    template_name = 'app_admin/clients_list.html'
    context_object_name = 'clients_list'

    def get_context_data(self, **kwargs):
        context = super(ClientsList, self).get_context_data(**kwargs)
        context['clients_group'] = app_admin_models.ClientsGroups.objects.get(id=self.kwargs["pk"]).title
        return context

    def get_queryset(self):
        return app_admin_models.Clients.objects.filter(select_clients_group_id=self.kwargs["pk"], deleted_user=False)


# Информация о клиенте
class ClientInfoView(admin_mixin.BaseAdminContentMixin, UpdateView):
    success_url = '/pythonix_admin/'
    model = app_admin_models.Clients
    context_object_name = 'client_info'
    template_name = 'app_admin/client_info.html'

    fields = ['first_name', 'last_name', 'email', 'username', 'ip_address', 'ipv6_address', 'send_sms', 'select_tarif',
              'select_clients_group', 'select_street', 'mobile_phone',
                'home_address', 'balance']

    def get_context_data(self, **kwargs):
        context = super(ClientInfoView, self).get_context_data(**kwargs)
        context['physical_networks'] = app_admin_models.PhysicalNetwork.objects.all()
        context['employees'] = app_admin_models.Employees.objects.filter(type_employees='installer')
        return context


    def form_valid(self, form):
        client = app_admin_models.Clients.objects.get(id=self.kwargs["pk"])
        if client.ip_address != form.cleaned_data['ip_address']:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.update_client_info_mikrotik.updateIP(server.network_address, server.api_port, server.login, server.password,
                    client.ip_address, form.cleaned_data['ip_address'])

                app_scripts.update_client_info_mikrotik.updatePPPIP(server.network_address, server.api_port, server.login, server.password,
                    client.ip_address, form.cleaned_data['ip_address'])

        if client.username != form.cleaned_data['username']:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.update_client_info_mikrotik.updateLogin(server.network_address, server.api_port, server.login, server.password,
                    client.username, form.cleaned_data['username'])

        self.success_url = '/pythonix_admin/client_info/'+self.kwargs["pk"]+'/'
        return super(ClientInfoView, self).form_valid(form)


# Отчет о пополнениях клиентов
class ReportPayAdminList(admin_mixin.BaseAdminContentMixin, ListView):

    template_name = 'app_admin/report_pay_list.html'
    context_object_name = 'report_pay_list'

    def get_queryset(self):
        return app_admin_models.ReportPayAdmin.objects.all()


# Определяем свободные IP для выбранных подсетей
def get_free_ipaddress(request, id):

    clients_group = app_admin_models.ClientsGroups.objects.get(id=id)

    clients_used_ip = [client.ip_address for client in app_admin_models.Clients.objects.filter(select_clients_group=clients_group, deleted_user=False)]
    json_ip_addresses = {}

    free_ip_list = []

    for network in clients_group.ipv4networks_list.all():

        for ip_address in iplib.CIDR(str(network.ipv4networks) + "/" + str(network.CIDR)):
            if ip_address not in clients_used_ip and ip_address != network.ipv4networks:
                json_ip_addresses.update({str(ip_address):str(ip_address)})
                break

    return HttpResponse(
        json.dumps(json_ip_addresses), content_type='application/json'
    )


# Определяем группы клиентов для выбранной физической сети
def get_client_groups(request, id):
    json_client_groups = {}
    server_list = [server.id for server in app_admin_models.Servers.objects.filter(physical_network=id)]
    for client_group in app_admin_models.ClientsGroups.objects.filter(select_server__in=server_list):
        json_client_groups.update({str(client_group.id):u'{}'.format(client_group.title)})
    return HttpResponse(
        json.dumps(json_client_groups), content_type='application/json'
    )


# Возвращяем абривиатуру физической сети
def abbreviation_physical_network(request, id):
    json_abbreviation = {}
    physical_network = app_admin_models.PhysicalNetwork.objects.get(id=id)
    json_abbreviation.update({'abbreviation':physical_network.abbreviation})
    return HttpResponse(
        json.dumps(json_abbreviation), content_type='application/json'
    )


# Определяем доступные группы клиентов,
def get_client_groups(request, id):
    json_client_groups = {}
    server_list = [server.id for server in app_admin_models.Servers.objects.filter(physical_network=id)]
    for client_group in app_admin_models.ClientsGroups.objects.filter(select_server__in=server_list):
        json_client_groups.update({str(client_group.id):u'{}'.format(client_group.title)})
    return HttpResponse(
        json.dumps(json_client_groups), content_type='application/json'
    )


# Обновление пароля
def update_password(request, id):
    try:
        app_admin_models.AdminProfile.objects.get(id=request.user.id)
    except:
        return HttpResponseRedirect("/")
    json_new_password = {}
    password, enctipt_password = make_password(password=get_random_string(9, '1234567890'),
                                  salt=None,
                                  hasher='unsalted_md5')
    json_new_password.update({'password':password})

    client = app_admin_models.Clients.objects.get(id=id)

    try:
        for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.update_client_info_mikrotik.updatePPPassword(server.network_address, server.api_port, server.login, server.password,
                    client.key, password)
    except:
        json_new_password.update({'password':'Сервер не доступен'})
    else:
        client.password = enctipt_password
        client.key = password
        client.save()
    return HttpResponse(
        json.dumps(json_new_password), content_type='application/json'
    )


# Пополнение баланса
def pay_balance(request, id, sum):
    try:
        admin = app_admin_models.AdminProfile.objects.get(id=request.user.id)
    except:
        return HttpResponseRedirect("/")
    json_balance = {}

    client = app_admin_models.Clients.objects.get(id=id)
    client.balance = client.balance + int(sum)

    if (int(client.balance)  >= 0):
        try:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.client_on_off.clientOn(server.network_address, server.api_port, server.login, server.password, client.ip_address)
                json_balance.update({'message':'Счет пополнен'})
        except:
            json_balance.update({'message':'Сервер не доступен'})
        else:
            client.internet_status = True
            client.save()

    else:
        json_balance.update({'message':'Недостаточно средств'})
        client.save()

    # Добавляем запись в отчет о пополнениях
    app_admin_models.ReportPayAdmin.objects.create(id_admin_select=admin, id_client_select=client,
        sum=sum)


    return HttpResponse(
        json.dumps(json_balance), content_type='application/json'
    )


# Включение отключение клиента
def client_on_off(request, id, action):
    try:
        admin = app_admin_models.AdminProfile.objects.get(id=request.user.id)
    except:
        return HttpResponseRedirect("/")
    json_client_on_off = {}

    client = app_admin_models.Clients.objects.get(id=id)

    if action == '0':
        try:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.client_on_off.clientOff(server.network_address, server.api_port, server.login, server.password, client.ip_address)
        except:
            json_client_on_off.update({'message':'Сервер не доступен'})
        else:
            json_client_on_off.update({'message':'Клиент отключен'})
    else:
        try:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.client_on_off.clientOn(server.network_address, server.api_port, server.login, server.password, client.ip_address)
        except:
            json_client_on_off.update({'message':'Сервер не доступен'})
        else:
            json_client_on_off.update({'message':'Клиент включен'})

    return HttpResponse(
        json.dumps(json_client_on_off), content_type='application/json'
    )



# Отправка данных о пользователе монтажнику
def sendSmsInfoClientAjax(request, client_id, employeer_id):
    try:
        admin = app_admin_models.AdminProfile.objects.get(id=request.user.id)
    except:
        return HttpResponseRedirect("/")

    employeer = app_admin_models.Employees.objects.get(id=employeer_id)
    client = app_admin_models.Clients.objects.get(id=client_id)
    text_sms = client.username + ' // ' + client.key + ' // ' + client.ip_address
    smsc.sendInfoEmployeer(employeer.mobile_phone, text_sms)
    json_sms_info = {}
    json_sms_info.update({'message':'ok'})

    return HttpResponse(
        json.dumps(json_sms_info), content_type='application/json'
    )


# Данные о подключении клиента
def getStatusClient(request, client_id):
    try:
        admin = app_admin_models.AdminProfile.objects.get(id=request.user.id)
    except:
        return HttpResponseRedirect("/")

    client = app_admin_models.Clients.objects.get(id=client_id)

    json_status_info = {}

    try:
        arp_records = 0
        for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
            if (app_scripts.client_status.getArp(server.network_address, server.api_port, server.login, server.password, client.ip_address) == True):
                arp_records += 1
    except:
        json_status_info.update({'message':'Сервер не доступен'})
    else:
        json_status_info.update({'message':'Данные получены'})
        if arp_records > 0:
            json_status_info.update({'arp':True})
        else:
            json_status_info.update({'arp':False})


    try:
        arp_records = 0
        for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
            if (app_scripts.client_status.getPPP(server.network_address, server.api_port, server.login, server.password, client.ip_address) == True):
                arp_records += 1
    except:
        json_status_info.update({'message':'Сервер не доступен'})
    else:
        json_status_info.update({'message':'Данные получены'})
        if arp_records > 0:
            json_status_info.update({'ppp':True})
        else:
            json_status_info.update({'ppp':False})

    return HttpResponse(
        json.dumps(json_status_info), content_type='application/json'
    )


# Удаление клиента
class ClientDelete(admin_mixin.BaseAdminContentMixin, FormView):

    form_class = forms.DelClientForm
    template_name = 'app_admin/delete_client.html'
    success_url = '/pythonix_admin/'

    def get_context_data(self, **kwargs):
        context = super(ClientDelete, self).get_context_data(**kwargs)
        context['client_id'] = self.kwargs.get('pk')
        context['title_message'] = "Удалить клиента"
        return context

    def form_valid(self, form):
        client = app_admin_models.Clients.objects.get(id=self.kwargs.get('pk'))

        try:
            for server in app_admin_models.Servers.objects.filter(physical_network=client.select_clients_group.select_server.physical_network):
                app_scripts.client_delete.deleteAddressList(server.network_address, server.api_port, server.login, server.password,
                    client.ip_address)

                app_scripts.client_delete.deletePPP(server.network_address, server.api_port, server.login, server.password,
                    client.ip_address)
        except:
            return HttpResponseRedirect('/pythonix_admin/')
        else:
            client.deleted_user = True
            client.save()
            return super(ClientDelete, self).form_valid(form)



#class SendSmsInfoClientAjax():
#    def dispatch(self, request, *args, **kwargs):
#        super(SendSmsInfoClientAjax, self).dispatch(request, *args, **kwargs)
#        data = {
#                'id_client': kwargs['id_client'],
#                'id_employeer':kwargs['id_employeer']
#            }
#        return JsonResponse(data)
