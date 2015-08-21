from django.db import models
from django.contrib.auth.models import User
from surveillance_cholera.models  import PhoneNumber #, Person
# Signal while saving user
from django.db.models.signals import post_save

class UserProfile(models.Model):
    MOH_LEVEL_CHOICES = (
        ('c', 'Central'),
        ('p', 'PBS'),
        ('b', 'BDS'),
        ('d', 'CDS'),
    )
    user = models.OneToOneField(User, primary_key=True)
    telephone = models.ForeignKey(PhoneNumber, null=True, blank=True)
    level= models.CharField(max_length=1, choices=MOH_LEVEL_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
