# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0005_patient_cds'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='exit_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 31, 12, 42, 56, 133986, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='exit_status',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
