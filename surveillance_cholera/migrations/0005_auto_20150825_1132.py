# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0004_auto_20150824_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cdsuser',
            name='cds',
        ),
        migrations.RemoveField(
            model_name='cdsuser',
            name='person',
        ),
        migrations.RemoveField(
            model_name='districtuser',
            name='district',
        ),
        migrations.RemoveField(
            model_name='districtuser',
            name='person',
        ),
        migrations.RemoveField(
            model_name='generaluser',
            name='cds',
        ),
        migrations.RemoveField(
            model_name='generaluser',
            name='person',
        ),
        migrations.RemoveField(
            model_name='provinceuser',
            name='person',
        ),
        migrations.RemoveField(
            model_name='provinceuser',
            name='province',
        ),
        migrations.DeleteModel(
            name='CDSUser',
        ),
        migrations.DeleteModel(
            name='DistrictUser',
        ),
        migrations.DeleteModel(
            name='GeneralUser',
        ),
        migrations.DeleteModel(
            name='ProvinceUser',
        ),
    ]
