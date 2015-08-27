# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date_entry',
            field=models.DateField(default=datetime.datetime(2015, 8, 27, 7, 56, 0, 85978, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
