# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_userprofile_moh_facility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='level',
            field=models.CharField(default=b'CDS', help_text='Either CDS, BDS, PBS, or Central level.', max_length=3, choices=[(b'CEN', b'Central'), (b'BPS', b'BPS'), (b'BDS', b'BDS'), (b'CDS', b'CDS')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='moh_facility',
            field=models.IntegerField(help_text='Code of the MoH facility', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='telephone',
            field=models.CharField(help_text='The telephone to contact you.', max_length=22),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, help_text='The general user'),
        ),
    ]
