# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import authentication.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telephone', models.CharField(default=b'+257', unique=True, max_length=22)),
                ('level', models.CharField(blank=True, max_length=3, null=True, choices=[(b'CEN', b'Central'), (b'BPS', b'BPS'), (b'BDS', b'BDS'), (b'CDS', b'CDS')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('objects', authentication.models.MyManager()),
            ],
        ),
    ]
