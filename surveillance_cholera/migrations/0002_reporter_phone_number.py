# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporter',
            name='phone_number',
            field=models.CharField(default='', max_length=12),
            preserve_default=False,
        ),
    ]
