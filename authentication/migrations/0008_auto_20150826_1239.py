# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20150826_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='telephone',
            field=models.CharField(blank=True, help_text='The telephone to contact you.', max_length=16, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]),
        ),
    ]
