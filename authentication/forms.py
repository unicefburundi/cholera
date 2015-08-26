from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from surveillance_cholera.models import CDS, District, Province
from django.utils.translation import ugettext as _

class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        exclude = ("user",)

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        level = cleaned_data['level']
        moh_facility = cleaned_data['moh_facility']
        if level == 'CDS':
            if CDS.objects.filter(name=moh_facility) is not []:
                self.add_error('moh_facility',_("CDS doesn't exit!"))
        elif level=='BDS':
            if District.objects.filter(name=moh_facility) is not []:
                self.add_error('moh_facility',_("BDS doesn't exit!"))
        elif level=='BPS':
            if Province.objects.filter(name=moh_facility) is not []:
                self.add_error('moh_facility',_("BPS doesn't exit!"))
        else:
            return True


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
