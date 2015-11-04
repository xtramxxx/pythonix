# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0005_auto_20150914_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employees',
            options={'verbose_name': '\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a', 'verbose_name_plural': '\u0421\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u0438'},
        ),
        migrations.AlterField(
            model_name='clients',
            name='end_used_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 21, 15, 20, 7, 250000), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd1\x8f\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x83\xd1\x81\xd0\xbb\xd1\x83\xd0\xb3\xd0\xb8'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='type_employees',
            field=models.CharField(max_length=50, verbose_name=b'\xd0\xa2\xd0\xb8\xd0\xbf \xd1\x81\xd0\xbe\xd1\x82\xd1\x80\xd1\x83\xd0\xb4\xd0\xbd\xd0\xb8\xd0\xba\xd0\xb0', choices=[(b'installer', '\u041c\u043e\u043d\u0442\u0430\u0436\u043d\u0438\u043a')]),
        ),
        migrations.AlterModelTable(
            name='employees',
            table='mployees',
        ),
    ]
