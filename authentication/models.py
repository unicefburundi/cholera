from django.db import models
from django.contrib.auth.models import User
from surveillance_cholera.models  import PhoneNumber #, Person

class UserProfile(models.Model):
    MOH_LEVEL_CHOICES = (
        ('c', 'Central'),
        ('p', 'PBS'),
        ('b', 'BDS'),
        ('d', 'CDS'),
    )
    user = models.OneToOneField(User, primary_key=True)
    telephone = models.ForeignKey(PhoneNumber)
    level= models.CharField(max_length=1, choices=MOH_LEVEL_CHOICES)
