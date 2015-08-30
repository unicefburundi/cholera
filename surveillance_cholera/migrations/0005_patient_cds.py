# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0004_auto_20150828_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='cds',
            field=models.ForeignKey(default=170302, to='surveillance_cholera.CDS'),
            preserve_default=False,
        ),
    ]
