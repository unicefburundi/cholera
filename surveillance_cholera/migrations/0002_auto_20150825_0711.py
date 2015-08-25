# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance_cholera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=-1, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.OneToOneField(to='authentication.UserProfile'),
        ),
    ]
