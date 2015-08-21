# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0002_reporter_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=12)),
                ('supervisor_phone_number', models.CharField(max_length=12)),
                ('cds', models.ForeignKey(to='surveillance_cholera.CDS')),
            ],
        ),
        migrations.RemoveField(
            model_name='session',
            name='report',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
