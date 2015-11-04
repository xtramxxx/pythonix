# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app_admin', '0002_auto_20150911_0119'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='key',
            field=models.CharField(default=b'000000000', max_length=50),
        ),
        migrations.AlterField(
            model_name='clients',
            name='end_used_date',
            field=models.DateField(default=datetime.datetime(2015, 9, 20, 13, 25, 42, 203000), verbose_name=b'\xd0\x94\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd1\x8f\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x83\xd1\x81\xd0\xbb\xd1\x83\xd0\xb3\xd0\xb8'),
        ),
    ]
