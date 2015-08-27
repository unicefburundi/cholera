# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0004_auto_20150827_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cds',
            name='status',
            field=models.CharField(blank=True, max_length=4, null=True, help_text='Either Public, Conf, Ass, Prive  or Hospital status.', choices=[(b'Pub', b'Public'), (b'Con', b'Conf'), (b'Priv', b'Prive'), (b'Ass', b'Ass'), (b'HPub', b'HPublic'), (b'HCon', b'HConf'), (b'HPrv', b'HPrive')]),
        ),
    ]
