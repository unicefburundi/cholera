# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20150823_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='telephone',
            field=models.CharField(max_length=22),
        ),
    ]
