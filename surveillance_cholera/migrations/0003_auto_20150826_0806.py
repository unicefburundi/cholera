# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0002_auto_20150825_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='code',
            field=models.CharField(unique=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(unique=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
