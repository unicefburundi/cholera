from django import template
import datetime
from surveillance_cholera.models import Patient

register = template.Library()
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

def format_to_time(date):
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    return d

def not_in_cds_group(user):
    if user:
        return user.groups.filter(name='CDS').count() == 0
    return False

def not_in_bds_group(user):
    if user:
        return user.groups.filter(name='BDS').count() == 0
    return False

def not_in_bps_group(user):
    if user:
        return user.groups.filter(name='BPS').count() == 0
    return False

def not_in_central_group(user):
    if user:
        return user.groups.filter(name='Central').count() == 0
    return False

def get_all_patients(level=None,moh_facility=None):
    if level=='CDS':
        return Patient.objects.filter(cds__code=moh_facility)
    if level=='BDS':
        return Patient.objects.filter(cds__district__code=moh_facility)
    if level =='BPS':
        return Patient.objects.filter(cds__district__province__code=moh_facility)
    else:
        return Patient.objects.all()