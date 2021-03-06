# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="CDS",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(max_length=40)),
                ("code", models.CharField(unique=True, max_length=6)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        max_length=4,
                        null=True,
                        help_text="Either Public, Conf, Ass, Prive  or Hospital status.",
                        choices=[
                            (b"Pub", b"Public"),
                            (b"Con", b"Conf"),
                            (b"Priv", b"Prive"),
                            (b"Ass", b"Ass"),
                            (b"HPub", b"HPublic"),
                            (b"HCon", b"HConf"),
                            (b"HPrv", b"HPrive"),
                        ],
                    ),
                ),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(unique=True, max_length=40)),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("patient_id", models.CharField(unique=True, max_length=50)),
                ("colline_name", models.CharField(max_length=50)),
                ("age", models.CharField(max_length=10)),
                ("sexe", models.CharField(max_length=10)),
                ("intervention", models.CharField(max_length=50)),
                ("date_entry", models.DateField(blank=True)),
                ("exit_date", models.DateField(null=True, blank=True)),
                ("exit_status", models.CharField(max_length=10, null=True, blank=True)),
                (
                    "cds",
                    models.ForeignKey(
                        blank=True, to="surveillance_cholera.CDS", null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                )
            ],
        ),
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("number", models.CharField(max_length=100)),
                ("person", models.ForeignKey(to="surveillance_cholera.Person")),
            ],
        ),
        migrations.CreateModel(
            name="Province",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("name", models.CharField(unique=True, max_length=20)),
                ("code", models.IntegerField(unique=True)),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("message", models.CharField(max_length=160)),
                ("report_type", models.CharField(max_length=30)),
                ("cds", models.ForeignKey(to="surveillance_cholera.CDS")),
                ("patient", models.ForeignKey(to="surveillance_cholera.Patient")),
            ],
        ),
        migrations.CreateModel(
            name="Reporter",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("phone_number", models.CharField(max_length=100)),
                ("supervisor_phone_number", models.CharField(max_length=100)),
                ("cds", models.ForeignKey(to="surveillance_cholera.CDS")),
            ],
        ),
        migrations.CreateModel(
            name="Temporary",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("phone_number", models.CharField(max_length=100)),
                ("supervisor_phone_number", models.CharField(max_length=100)),
                ("cds", models.ForeignKey(to="surveillance_cholera.CDS")),
            ],
        ),
        migrations.CreateModel(
            name="TrackPatientMessage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("exit_date", models.DateField()),
                ("exit_status", models.CharField(max_length=20)),
                ("report", models.ForeignKey(to="surveillance_cholera.Report")),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
                        blank=True,
                        help_text="The telephone to contact you.",
                        max_length=16,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex=b"^\\+?1?\\d{9,15}$",
                                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                            )
                        ],
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        blank=True,
                        help_text="Either CDS, BDS, PBS, or Central level.",
                        max_length=3,
                        choices=[
                            (b"CEN", b"Central"),
                            (b"BPS", b"BPS"),
                            (b"BDS", b"BDS"),
                            (b"CDS", b"CDS"),
                        ],
                    ),
                ),
                (
                    "moh_facility",
                    models.CharField(
                        help_text="Code of the MoH facility",
                        max_length=8,
                        null=True,
                        blank=True,
                    ),
                ),
                ("user", models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("user",)},
        ),
        migrations.AddField(
            model_name="report",
            name="reporter",
            field=models.ForeignKey(to="surveillance_cholera.Reporter"),
        ),
        migrations.AddField(
            model_name="person",
            name="user",
            field=models.OneToOneField(to="surveillance_cholera.UserProfile"),
        ),
        migrations.AddField(
            model_name="district",
            name="province",
            field=models.ForeignKey(to="surveillance_cholera.Province"),
        ),
        migrations.AddField(
            model_name="cds",
            name="district",
            field=models.ForeignKey(to="surveillance_cholera.District"),
        ),
    ]
