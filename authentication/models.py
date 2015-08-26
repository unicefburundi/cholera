from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _

class MyManager(models.Manager):
    use_in_migrations = True

class UserProfile(models.Model):
    MOH_LEVEL_CHOICES = (
        ('CEN', 'Central'),
        ('BPS', 'BPS'),
        ('BDS', 'BDS'),
        ('CDS', 'CDS'),
    )
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, help_text=_('The general user'))
    # The additional attributes we wish to include.
    telephone = models.CharField(max_length=22, help_text=_('The telephone to contact you.'))
    level= models.CharField(max_length=3, choices=MOH_LEVEL_CHOICES, default=MOH_LEVEL_CHOICES[3][0], help_text=_('Either CDS, BDS, PBS, or Central level.'))
    moh_facility = models.IntegerField(null=True, blank=True, help_text=_('Code of the MoH facility'))

    def __unicode__(self):
        return "%s's profile" % self.user

    objects = MyManager()

    def user_email(self, instance):
        return instance.user.email

    def user_firstname(self, instance):
        return instance.user.first_name

    def user_lastname(self, instance):
        return instance.user.last_name



def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
