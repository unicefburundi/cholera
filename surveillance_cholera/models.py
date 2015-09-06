from django.db import models
from authentication.models import UserProfile
from django.utils.translation import ugettext as _

class Person(models.Model):
    user = models.OneToOneField(UserProfile)

    def __unicode__(self):
            return self.user.user.username

class PhoneNumber(models.Model):
    number = models.CharField(max_length=100)
    person = models.ForeignKey(Person)

    def __unicode__(self):
            return self.number


class Province(models.Model):
    name = models.CharField(unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class District(models.Model):
    province = models.ForeignKey(Province)
    name = models.CharField(unique=True, max_length=40)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class CDS(models.Model):
    STATUS_CHOICES = (
        ('Pub', 'Public'),
        ('Con', 'Conf'),
        ('Priv', 'Prive'),
        ('Ass', 'Ass'),
        ('HPub', 'HPublic'),
        ('HCon', 'HConf'),
        ('HPrv', 'HPrive'),
    )
    district = models.ForeignKey(District)
    name = models.CharField( max_length=40)
    code = models.CharField(unique=True, max_length=6)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=True, null=True, help_text=_('Either Public, Conf, Ass, Prive  or Hospital status.'))

    def __unicode__(self):
        return self.name

class Patient(models.Model):
    cds = models.ForeignKey(CDS, null=True, blank=True)
    patient_id = models.CharField(unique=True, max_length=50)
    colline_name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    sexe = models.CharField(max_length=10)
    intervention = models.CharField(max_length=50)
    date_entry = models.DateField(blank=True)
    exit_date = models.DateField(blank=True, null=True)
    exit_status = models.CharField(max_length=10, blank=True, null = True)

    def __unicode__(self):
            return self.patient_id

class Reporter(models.Model):
    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=100)
    supervisor_phone_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.phone_number

class Report(models.Model):
    patient = models.ForeignKey(Patient)
    reporter = models.ForeignKey(Reporter)
    cds = models.ForeignKey(CDS)
    message = models.CharField(max_length=160)
    report_type = models.CharField(max_length=30)

    def __unicode__(self):
        return self.message

class TrackPatientMessage(models.Model):
    report = models.ForeignKey(Report)
    exit_date = models.DateField()
    exit_status = models.CharField(max_length=20)


class Temporary(models.Model):
    '''
    This model will be used to temporary store a reporter who doesn't finish his self registration
    '''
    cds = models.ForeignKey(CDS)
    phone_number = models.CharField(max_length=100)
    supervisor_phone_number = models.CharField(max_length=100)

    def __unicode__(self):
        return self.phone_number


