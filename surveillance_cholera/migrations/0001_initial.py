# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CDS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='CDSUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('cds', models.ForeignKey(to='surveillance_cholera.CDS')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='DistrictUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('district', models.ForeignKey(to='surveillance_cholera.District')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('cds', models.ForeignKey(to='surveillance_cholera.CDS')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('patient_id', models.CharField(max_length=50)),
                ('colline_name', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=10)),
                ('sexe', models.CharField(max_length=10)),
                ('intervention', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=12)),
                ('person', models.ForeignKey(to='surveillance_cholera.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProvinceUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
                ('person', models.ForeignKey(to='surveillance_cholera.Person')),
                ('province', models.ForeignKey(to='surveillance_cholera.Province')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=160)),
                ('report_type', models.CharField(max_length=10)),
                ('cds', models.ForeignKey(to='surveillance_cholera.CDS')),
                ('patient', models.ForeignKey(to='surveillance_cholera.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supervisor_phone_number', models.CharField(max_length=12)),
                ('cds', models.ForeignKey(to='surveillance_cholera.CDS')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operation', models.CharField(max_length=10)),
                ('level', models.IntegerField()),
                ('report', models.ForeignKey(to='surveillance_cholera.Reporter')),
            ],
        ),
        migrations.CreateModel(
            name='TrackPatientMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exit_date', models.DateField()),
                ('exit_status', models.CharField(max_length=20)),
                ('report', models.ForeignKey(to='surveillance_cholera.Reporter')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='reporter',
            field=models.ForeignKey(to='surveillance_cholera.Reporter'),
        ),
        migrations.AddField(
            model_name='generaluser',
            name='person',
            field=models.ForeignKey(to='surveillance_cholera.Person'),
        ),
        migrations.AddField(
            model_name='districtuser',
            name='person',
            field=models.ForeignKey(to='surveillance_cholera.Person'),
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(to='surveillance_cholera.Province'),
        ),
        migrations.AddField(
            model_name='cdsuser',
            name='person',
            field=models.ForeignKey(to='surveillance_cholera.Person'),
        ),
        migrations.AddField(
            model_name='cds',
            name='district',
            field=models.ForeignKey(to='surveillance_cholera.District'),
        ),
    ]
