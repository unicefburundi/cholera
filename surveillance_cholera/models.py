from django.db import models

# Create your models here.

class Person(models.Model):
        first_name = models.CharField(max_length=80)
        last_name = models.CharField(max_length=80)
        email = models.CharField(max_length=50)
        def __unicode__(self):
                name = self.first_name+' '+self.last_name
                return name
	
class PhoneNumber(models.Model):
	number = models.CharField(max_length=12)
	person = models.ForeignKey(Person)

class Patient(models.Model):
	patient_id = models.CharField(max_length=50)
	colline_name = models.CharField(max_length=50)
	age = models.CharField(max_length=10)
	sexe = models.CharField(max_length=10)
	intervention = models.CharField(max_length=50)

class Province(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
                name = self.name
                return name

class District(models.Model):
	name = models.CharField(max_length=40)
	province = models.ForeignKey(Province)
	def __unicode__(self):
                name = self.name
                return name

class CDS(models.Model):
	name = models.CharField(max_length=40)
	code = models.CharField(max_length=6)
	district = models.ForeignKey(District)
	def __unicode__(self):
		name = self.name
		return name

class Reporter(models.Model):
	phone_number = models.CharField(max_length=12)
	cds = models.ForeignKey(CDS)
	supervisor_phone_number = models.CharField(max_length=12)

class Report(models.Model):
	patient = models.ForeignKey(Patient)
	reporter = models.ForeignKey(Reporter)
	cds = models.ForeignKey(CDS)
	message = models.CharField(max_length=160)
	report_type = models.CharField(max_length=10)

class TrackPatientMessage(models.Model):
	exit_date = models.DateField()
	exit_status = models.CharField(max_length=20)
	report = models.ForeignKey(Reporter)

class GeneralUser(models.Model):
	person = models.ForeignKey(Person)
	cds = models.ForeignKey(CDS)
	login = models.CharField(max_length=40)
	password = models.CharField(max_length=40)


class ProvinceUser(models.Model):
	person = models.ForeignKey(Person)
	province = models.ForeignKey(Province)
	login = models.CharField(max_length=40)
        password = models.CharField(max_length=40)

class DistrictUser(models.Model):
	person = models.ForeignKey(Person)
	district = models.ForeignKey(District)
        login = models.CharField(max_length=40)
        password = models.CharField(max_length=40)

class CDSUser(models.Model):
	person = models.ForeignKey(Person)
	cds = models.ForeignKey(CDS)
        login = models.CharField(max_length=40)
        password = models.CharField(max_length=40)

class Temporary(models.Model):
	'''This model will be used to temporary store a reporter who doesn't finish his self registration'''
	phone_number = models.CharField(max_length=12)
	cds = models.ForeignKey(CDS)
	supervisor_phone_number = models.CharField(max_length=12)

	
