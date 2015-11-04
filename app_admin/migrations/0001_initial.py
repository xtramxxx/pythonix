# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('admin_status', models.BooleanField(default=True, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0')),
                ('permissions_role', models.IntegerField(default=1, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80 \xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd0\xbb\xd0\xb5\xd0\xb3\xd0\xb8\xd0\xb9 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb0', choices=[(b'1', b'All action'), (b'2', b'See, Add, Edit, Del  Clients'), (b'3', b'See Report'), (b'4', b'Generated card'), (b'5', b'See client')])),
            ],
            options={
                'db_table': 'admin_profile',
                'verbose_name': 'AdminProfile',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
