# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0003_auto_20150824_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackpatientmessage',
            name='report',
            field=models.ForeignKey(to='surveillance_cholera.Report'),
        ),
    ]
