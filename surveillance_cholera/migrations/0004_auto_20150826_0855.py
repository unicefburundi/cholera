# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0003_auto_20150826_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='district',
            name='code',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='province',
            name='code',
            field=models.IntegerField(default=23, unique=True),
            preserve_default=False,
        ),
    ]
