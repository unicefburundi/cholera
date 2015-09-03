# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='phone_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reporter',
            name='supervisor_phone_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='temporary',
            name='phone_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='temporary',
            name='supervisor_phone_number',
            field=models.CharField(max_length=100),
        ),
    ]
