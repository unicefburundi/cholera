# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0006_auto_20150831_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='exit_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='exit_status',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
