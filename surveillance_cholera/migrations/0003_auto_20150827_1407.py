# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0002_patient_entry_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='entry_date',
        ),
        migrations.AddField(
            model_name='cds',
            name='status',
            field=models.CharField(blank=True, max_length=4, null=True, help_text='Either Public, Conf, Ass, Prive  or Hospital status.', choices=[(b'Pub', b'Public'), (b'Con', b'Conf'), (b'Priv', b'Prive'), (b'Ass', b'Ass'), (b'HPub', b'HPublic'), (b'HCon', b'HConf'), (b'HPrv', b'HPrive')]),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_entry',
            field=models.DateField(default=datetime.datetime(2015, 8, 27, 12, 7, 35, 177203, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
