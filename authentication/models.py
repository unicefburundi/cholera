from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator

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
    user = models.OneToOneField(User, primary_key=True, help_text=_('The general user'))
    # The additional attributes we wish to include.
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    telephone = models.CharField(validators=[phone_regex], blank=True, help_text=_('The telephone to contact you.'), max_length=16)
    level= models.CharField(max_length=3, choices=MOH_LEVEL_CHOICES, blank=True, help_text=_('Either CDS, BDS, PBS, or Central level.'))
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
