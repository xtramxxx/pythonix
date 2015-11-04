# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0006_auto_20150914_1520'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('secret_code', models.CharField(default='632754386472338', unique=True, max_length=50, verbose_name=b'\xd0\xa1\xd0\xb5\xd0\xba\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xba\xd0\xbe\xd0\xb4')),
                ('par_card', models.IntegerField(verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb0\xd0\xbb \xd0\xba\xd0\xb0\xd1\x80\xd1\x82\xd0\xbe\xd1\x87\xd0\xba\xd0\xb8')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('used_date', models.DateField(verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f', blank=True)),
                ('used', models.BooleanField(default=False, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd0\xb8\xd1\x81\xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
            ],
            options={
                'db_table': 'pay_card',
                'verbose_name': '\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0430 \u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f',
                'verbose_name_plural': '\u041a\u0430\u0440\u0442\u043e\u0447\u043a\u0438 \u043f\u043e\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.AlterField(
            model_name='clients',
            name='end_used_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 23, 15, 39, 27, 528000), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd1\x8f\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x83\xd1\x81\xd0\xbb\xd1\x83\xd0\xb3\xd0\xb8'),
        ),
    ]
