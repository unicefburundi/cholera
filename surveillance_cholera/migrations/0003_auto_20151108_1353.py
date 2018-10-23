# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("surveillance_cholera", "0002_auto_20151108_1349")]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="level",
            field=models.CharField(
                blank=True,
                help_text="Either CDS, BDS, PBS, or Central level.",
                max_length=7,
                choices=[
                    (b"Central", b"Central"),
                    (b"BPS", b"BPS"),
                    (b"BDS", b"BDS"),
                    (b"CDS", b"CDS"),
                ],
            ),
        )
    ]
