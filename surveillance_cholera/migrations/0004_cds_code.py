# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0003_auto_20150820_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='cds',
            name='code',
            field=models.CharField(default='', max_length=6),
            preserve_default=False,
        ),
    ]
