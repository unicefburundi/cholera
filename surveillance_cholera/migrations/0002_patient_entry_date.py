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
            name='entry_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 27, 9, 13, 58, 966644, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
