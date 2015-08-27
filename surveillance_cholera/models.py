from django.db import models
from authentication.models import UserProfile

class Person(models.Model):
    user = models.OneToOneField(UserProfile)

    def __unicode__(self):
            return self.user.user.username

class PhoneNumber(models.Model):
    number = models.CharField(max_length=12)
    person = models.ForeignKey(Person)

    def __unicode__(self):
            return self.number


class Patient(models.Model):
    patient_id = models.CharField(unique=True, max_length=50)
    colline_name = models.CharField(max_length=50)
    age = models.CharField(max_length=10)
    sexe = models.CharField(max_length=10)
    intervention = models.CharField(max_length=50)
    date_entry = models.DateField(auto_now_add=True, blank=True)

    def __unicode__(self):
            return self.patient_id

class Province(models.Model):
    name = models.CharField(unique=True, max_length=20)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class District(models.Model):
    name = models.CharField(unique=True, max_length=40)
    province = models.ForeignKey(Province)
    code = models.IntegerField(unique=True)

    def __unicode__(self):
        return self.name

class CDS(models.Model):
    name = models.CharField( max_length=40)
    district = models.ForeignKey(District)
    code = models.CharField(unique=True, max_length=6)

    def __unicode__(self):
        return self.name


class Reporter(models.Model):
    phone_number = models.CharField(max_length=12)
    cds = models.ForeignKey(CDS)
    supervisor_phone_number = models.CharField(max_length=12)

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
    exit_date = models.DateField()
    exit_status = models.CharField(max_length=20)
    report = models.ForeignKey(Report)



#class GeneralUser(models.Model):
#    person = models.ForeignKey(Person)
#    cds = models.ForeignKey(CDS)
#    login = models.CharField(max_length=40)
#    password = models.CharField(max_length=40)

#    def __unicode__(self):
#        return self.person


#class ProvinceUser(models.Model):
#    person = models.ForeignKey(Person)
#    province = models.ForeignKey(Province)
#    login = models.CharField(max_length=40)
#    password = models.CharField(max_length=40)

#    def __unicode__(self):
#        return self.login

#class DistrictUser(models.Model):
#    person = models.ForeignKey(Person)
#    district = models.ForeignKey(District)
#    login = models.CharField(max_length=40)
#    password = models.CharField(max_length=40)

#    def __unicode__(self):
#        return self.district

#class CDSUser(models.Model):
#    person = models.ForeignKey(Person)
#    cds = models.ForeignKey(CDS)
#    login = models.CharField(max_length=40)
#    password = models.CharField(max_length=40)

#    def __unicode__(self):
#        return self.person

#class Session(models.Model):
#    report = models.ForeignKey(Reporter)
#    operation = models.CharField(max_length=10)
#    level = models.IntegerField()

#    def __unicode__(self):
#        return self.report

class Temporary(models.Model):
    '''
    This model will be used to temporary store a reporter who doesn't finish his self registration
    '''
    phone_number = models.CharField(max_length=12)
    cds = models.ForeignKey(CDS)
    supervisor_phone_number = models.CharField(max_length=12)

    def __unicode__(self):
        return self.phone_number

