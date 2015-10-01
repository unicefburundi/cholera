# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0003_auto_20150930_1638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cds',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ('name',)},
        ),
    ]
