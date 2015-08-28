# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0003_auto_20150827_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_entry',
            field=models.DateField(blank=True),
        ),
    ]
