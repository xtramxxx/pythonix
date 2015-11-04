# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0003_auto_20150913_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportPayAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sum', models.IntegerField(verbose_name=b'\xd0\xa1\xd1\x83\xd0\xbc\xd0\xbc\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('date_of_refill', models.DateField(auto_now_add=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('id_admin_select', models.ForeignKey(verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80 \xd0\x90\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0', to='app_admin.AdminProfile')),
            ],
            options={
                'db_table': 'report_pay_admin',
                'verbose_name': '\u041f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u043e\u043c',
                'verbose_name_plural': '\u041f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u0435 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u043e\u043c',
            },
        ),
        migrations.AlterField(
            model_name='clients',
            name='end_used_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 20, 22, 48, 20, 649000), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd1\x8f\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x83\xd1\x81\xd0\xbb\xd1\x83\xd0\xb3\xd0\xb8'),
        ),
        migrations.AddField(
            model_name='reportpayadmin',
            name='id_client_select',
            field=models.ForeignKey(verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80 \xd0\x9a\xd0\xbb\xd0\xb8\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0', to='app_admin.Clients'),
        ),
    ]
