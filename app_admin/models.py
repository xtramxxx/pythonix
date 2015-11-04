# coding: utf-8
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

import random
import datetime

import app_scripts.tarifs_mikrotik


class AdminProfile(User):
    objects = UserManager()

    permissions = (
        (1, 'All action'),
        (2, 'See, Add, Edit, Del  Clients'),
        (3, 'See Report'),
        (4, 'Generated card'),
        (5, 'See client')
        )

    admin_status = models.BooleanField(verbose_name='Статус администратора', default=True)
    permissions_role = models.IntegerField(verbose_name='Выбор привелегий доступа', default=1, choices=permissions)


    class Meta:
        verbose_name = u'Профиль администратора'
        verbose_name_plural = u'Профили администраторов'
        db_table = "admin_profile"


    def __unicode__(self):
        return '{}'.format(self.username)


# Физическая сеть
class PhysicalNetwork(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название физической сети')
    select_admin = models.ManyToManyField(User, verbose_name='Выбор администратора')
    abbreviation = models.CharField(max_length=150, verbose_name='Аббревиатура физической сети')
    channel_width = models.IntegerField(verbose_name='Ширина канала', blank=True)

    class Meta:
        verbose_name = u'Физическая сеть'
        verbose_name_plural = u'Физические сети'
        db_table = 'physical_network'

    def __unicode__(self):
        return u'{}'.format(self.name)


# Сервера
class Servers(models.Model):
    SERVER_OS = (
        (1, 'MikroTik RouterOS'),
    )

    title = models.CharField(max_length=150, verbose_name='Название Сервера')
    physical_network = models.ForeignKey(PhysicalNetwork, verbose_name='Выбор физической сети')
    device_type = models.IntegerField(verbose_name='Выбор операционной системы', default=1, choices=SERVER_OS)
    network_address = models.GenericIPAddressField(verbose_name='Сетевой адрес устройства')
    login = models.CharField(max_length=50, verbose_name='Логин для доступа к устройству')
    password = models.CharField(max_length=50, verbose_name='Пароль для доступа к устройству')
    api_port = models.IntegerField(verbose_name='API порт', default=8728)
    status_on_off = models.BooleanField(verbose_name='Состояние работы сервера', default=True)

    class Meta:
        verbose_name = u'Сервер'
        verbose_name_plural = u'Сервера'
        db_table = 'device'

    def __unicode__(self):
        return u'{}'.format(self.title)


# IP Подсети v4
class IPV4Networks(models.Model):

    MASK_CHOICES = (
    (1, '1'),(2, '2'),(3, '3'),(4, '4'),(5, '5'),(6, '6'),(7, '7'),(8, '8'),(9, '9'),(10, '10'),(11, '11'),
    (12, '12'),(13, '13'),(14, '14'),(15, '15'),(16, '16'),(17, '17'),(18, '18'),(19, '19'),(20, '20'),
    (21, '21'),(22, '22'),(23, '23'),(24, '24'),(25, '25'),(26, '26'),(27, '27'),(28, '28'),(29, '29'),
    (30, '30'),(31, '31'),(32, '32'),
    )

    ipv4networks = models.GenericIPAddressField(verbose_name='IP Подсети')
    CIDR = models.IntegerField(choices=MASK_CHOICES, default=24)

    class Meta:
        verbose_name = u"Подсеть IPv4"
        verbose_name_plural = u'Список подсетей IPv4'
        db_table = "ip_v4_networks"

    def __unicode__(self):
        return u'{}'.format(self.ipv4networks)


# Группы клиентов
class ClientsGroups(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название группы')
    ipv4networks_list = models.ManyToManyField(IPV4Networks, verbose_name='Список подсетей IPv4')
    select_admin = models.ManyToManyField(User, verbose_name='Выбор администратора')
    select_server = models.ForeignKey(Servers, verbose_name='Выбор сервера')

    class Meta:
        verbose_name = u'Группа клиентов'
        verbose_name_plural = u'Группы клиентов'
        db_table = 'clients_groups'

    def __unicode__(self):
        return u'{}'.format(self.title)


# Тарифы
class Tarifs(models.Model):
    UNIT_SPEED = (
    ('k', 'k'),('M', 'M'),
    )

    select_physicalnetwork = models.ForeignKey(PhysicalNetwork, verbose_name='Выбор физической сети')
    title = models.CharField(max_length=150, verbose_name='Название тарифа')
    speed_up = models.IntegerField(verbose_name='Исходящая скорость, значение')
    speed_down = models.IntegerField(verbose_name='Входящая скорость, значение')
    speed_up_unit = models.CharField(max_length=1, verbose_name='Исходящая скорость, единица измерения', choices=UNIT_SPEED)
    speed_down_unit = models.CharField(max_length=1, verbose_name='Входящая скорость, единица измерения', choices=UNIT_SPEED)
    price = models.IntegerField(verbose_name='Абонплата')
    speed_limit = models.BooleanField(verbose_name='Лимитирование скорости', default=False)
    limit_rule = models.CharField(max_length=200, verbose_name='Правило, лимита', blank=True, null=True,)
    add_rule_in_device = models.BooleanField(verbose_name='Создавать ли правила в устройстве', default=True)

    class Meta:
        verbose_name = u'Тариф'
        verbose_name_plural = u'Тарифы'
        db_table = 'tarifs'

    def __unicode__(self):
        return u'{}'.format(self.title)

    def get_actions(self, request):
        actions = super(Tarifs, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save(self, *args, **kwargs):
        super(Tarifs, self).save(*args, **kwargs)
        for server in Servers.objects.filter(physical_network=self.select_physicalnetwork):
            app_scripts.tarifs_mikrotik.createTarifAddQueue(server.network_address, server.api_port,
                server.login, server.password, self.speed_up, self.speed_up_unit, self.speed_down, self.speed_down_unit)


    def delete(self, using=None):
        for server in Servers.objects.filter(physical_network=self.select_physicalnetwork):
            app_scripts.tarifs_mikrotik.deleteTarifAndQueue(server.network_address, server.api_port,
                server.login, server.password, self.speed_up, self.speed_up_unit, self.speed_down, self.speed_down_unit)
        super(Tarifs, self).delete(using)




# Улицы
class Streets(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название улицы')
    select_physical_network = models.ForeignKey(PhysicalNetwork, verbose_name='Выбор физической сети')


    class Meta:
        verbose_name = u'Улицу'
        verbose_name_plural = u'Улицы'
        db_table = 'streets'

    def __unicode__(self):
        return u'{}'.format(self.title)


# Клиенты
class Clients(User):
    objects = UserManager()

    ip_address = models.GenericIPAddressField(verbose_name='IP адрес клиена')
    ipv6_address = models.GenericIPAddressField(verbose_name='IPv6 адрес клиена', default="2001:0db8:11a3:09d7:1f34:8a2e:07a0:765d")
    send_sms = models.BooleanField(verbose_name='Желание получать смс', default=False)
    select_tarif = models.ForeignKey(Tarifs, verbose_name='Выбор тарифа')
    select_clients_group = models.ForeignKey(ClientsGroups, verbose_name='Выбор группы клиентов')
    create_date = models.DateField(verbose_name='Дата подключения', auto_now_add=True)
    end_used_date = models.DateField(verbose_name='Дата окончяния услуги', default=(datetime.datetime.now() + datetime.timedelta(days=7)))
    select_street = models.ForeignKey(Streets, verbose_name='Выбор улицы')
    mobile_phone = models.CharField(max_length=50, verbose_name='Мобильный телефон', blank=True, null=True,)
    home_address = models.CharField(max_length=50, verbose_name='Домашний адрес', blank=True, null=True,)
    network_traffic_per_day = models.IntegerField(verbose_name='Сетевой трафик за день', null=True, default=0)
    network_traffic_for_the_month = models.IntegerField(verbose_name='Сетевой трафик за месяц', null=True, default=0)
    balance = models.IntegerField(verbose_name='Баланс', default=0)
    internet_status = models.BooleanField(verbose_name='Статус клиента, доступ разрешен/запрещен', default=1)
    error_card = models.IntegerField(verbose_name='Ошибки пополнения карточкой', null=True, default=0)
    deleted_user = models.BooleanField(default=False, verbose_name='Статус удаления пользователя')
    key = models.CharField(max_length=50, default="000000000")

    class Meta:
        verbose_name = u"Клиент"
        verbose_name_plural = u"Клиенты"
        db_table = "clients"

    def __unicode__(self):
        return u'{} {} {} {} {}'.format(self.first_name, self.last_name, self.select_clients_group, self.ip_address, self.deleted_user)


# Модель отчета пополнений администраторами
class ReportPayAdmin(models.Model):
    id_admin_select = models.ForeignKey(AdminProfile, verbose_name='Выбор Администратора')
    id_client_select = models.ForeignKey(Clients, verbose_name='Выбор Клиента')
    sum = models.IntegerField(verbose_name='Сумма пополнения')
    date_of_refill = models.DateField(verbose_name='Дата пополнения', auto_now_add=True)

    class Meta:
        verbose_name = u"Пополнение администратором"
        verbose_name_plural = u"Пополнение администратором"
        db_table = "report_pay_admin"

    def __unicode__(self):
        return u'{} {} {} {}'.format(self.id_admin_select.first_name,
                                     self.id_client_select.first_name, self.sum, self.date_of_refill)


# Временные платежи
#class TemporaryPayment(models.Model):
#    select_client = models.ForeignKey(Clients, verbose_name='Выбор клиента')
#    sum = models.IntegerField(verbose_name='Сумма пополнения')
#    namber_days = models.IntegerField(verbose_name='Количество дней')
#    date_of_create = models.DateField(verbose_name='Дата создания платежа')
#    status = models.BooleanField(verbose_name='Состояние временного платежв', default=True)

#    class Meta:
#        verbose_name = u"Временный платеж"
#        verbose_name_plural = u"Временные платежи"
#        db_table = "temporary_payment"

#    def __unicode__(self):
#        return u'{}'.format(self.select_client,)


# Модель карточек
class Card(models.Model):
    secret_code = models.CharField(max_length=50, verbose_name='Секредный код', unique=True,)
    par_card = models.IntegerField(verbose_name='Номинал карточки')
    create_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    used_date = models.DateField(verbose_name='Дата использования', auto_now_add=True)
    used = models.BooleanField(verbose_name='Статус использования', default=False)

    class Meta:
        verbose_name = u"Карточка пополнения"
        verbose_name_plural = u"Карточки пополнения"
        db_table = "pay_card"

    def __unicode__(self):
        return u'{} {}'.format(self.par_card, self.secret_code)


# Абстрактный клас для генерации карточек
class GenCardModel(models.Model):

    def f_gen_card(self, count_card, par_card):
        current_count = 0

        while (current_count < int(count_card)):
            Card.objects.create(par_card=par_card, secret_code=get_random_string(15,allowed_chars='123456789'))
            current_count += 1

    class Meta:
        abstract = True


# Модель отчета использования карточек
#class CardReportUsed(models.Model):
#    client_used_card = models.CharField(max_length=100, verbose_name='Клиент использовавший карточку')
#    used_date = models.DateField(verbose_name='Дата использования')
#   id_card = models.ForeignKey(Card, verbose_name='ID проданной карточки')

#    class Meta:
#        db_table = "card_report_used"


# Модель определения новой даты
class NewDate(models.Model):
    def f_new_date(self, old_date):
        from datetime import datetime
        old_date_string = old_date

        split_date = str(old_date_string).split('-')

        if (int(split_date[1])+1) > 12:
            split_date = (str(int(split_date[0])+1) + "-" + "01" + "-" + split_date[2]).split('-')
        else:
            split_date = (str(split_date[0]) + "-" + str(int(split_date[1])+1) + "-" + split_date[2]).split('-')


        try:
            dt_obj = datetime(int(split_date[0]), int(split_date[1]), int(split_date[2]), )
            date_str = dt_obj.strftime("%Y-%m-%d")
            return date_str
        except:
            dt_obj = datetime(int(split_date[0]), int(split_date[1]) + 1, 1, )
            date_str = dt_obj.strftime("%Y-%m-%d")
            return date_str

    class Meta:
        abstract = True


# Сотрудники
class Employees(User):
    objects = UserManager()

    type_employees_list = (
            ('installer', u'Монтажник'),
        )

    status = models.BooleanField(verbose_name='Работает ли сотрудник', default=True)
    type_employees = models.CharField(max_length=50, verbose_name='Тип сотрудника', choices=type_employees_list)
    mobile_phone = models.CharField(max_length=50, verbose_name='Мобильный телефон')

    class Meta:
        verbose_name = u"Сотрудник"
        verbose_name_plural = u"Сотрудники"
        db_table = "mployees"

    def __unicode__(self):
        return u'{} {}'.format(self.first_name, self.last_name)