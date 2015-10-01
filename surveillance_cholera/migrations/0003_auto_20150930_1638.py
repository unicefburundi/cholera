# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0002_auto_20150903_0854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ('name',)},
        ),
    ]
