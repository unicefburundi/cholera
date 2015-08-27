# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0002_patient_date_entry'),
    ]

    operations = [
        migrations.AddField(
            model_name='cds',
            name='status',
            field=models.CharField(blank=True, help_text='Either Public, Conf, Ass, or Prive  status.', max_length=4, choices=[(b'Pub', b'Public'), (b'Con', b'Conf'), (b'Priv', b'Prive'), (b'Ass', b'Ass')]),
        ),
    ]
