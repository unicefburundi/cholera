# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("surveillance_cholera", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="level",
            field=models.CharField(
                blank=True,
                help_text="Either CDS, BDS, PBS, or Central level.",
                max_length=3,
                choices=[
                    (b"Central", b"Central"),
                    (b"BPS", b"BPS"),
                    (b"BDS", b"BDS"),
                    (b"CDS", b"CDS"),
                ],
            ),
        )
    ]
