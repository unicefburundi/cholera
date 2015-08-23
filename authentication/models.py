from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class MyManager(models.Manager):
    use_in_migrations = True

class UserProfile(models.Model):
    MOH_LEVEL_CHOICES = (
        ('CEN', 'Central'),
        ('BPS', 'BPS'),
        ('BDS', 'BDS'),
        ('CDS', 'CDS'),
    )
    user = models.OneToOneField(User)
    telephone = models.CharField(max_length=22)
    level= models.CharField(max_length=3, choices=MOH_LEVEL_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user

    objects = MyManager()


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
