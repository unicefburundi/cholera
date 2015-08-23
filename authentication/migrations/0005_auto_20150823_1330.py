# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20150823_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='level',
            field=models.CharField(default=b'CDS', max_length=3, choices=[(b'CEN', b'Central'), (b'BPS', b'BPS'), (b'BDS', b'BDS'), (b'CDS', b'CDS')]),
        ),
    ]
