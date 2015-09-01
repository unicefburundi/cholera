# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
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
                ('telephone', models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('level', models.CharField(blank=True, help_text='Either CDS, BDS, PBS, or Central level.', max_length=3, choices=[(b'CEN', b'Central'), (b'BPS', b'BPS'), (b'BDS', b'BDS'), (b'CDS', b'CDS')])),
                ('moh_facility', models.IntegerField(help_text='Code of the MoH facility', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text='The general user')),
            ],
            managers=[
                ('objects', authentication.models.MyManager()),
            ],
        ),
    ]
