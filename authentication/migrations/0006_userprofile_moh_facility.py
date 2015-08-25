# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20150823_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='moh_facility',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
