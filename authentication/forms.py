from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_(u'First Name'), max_length=30)
    last_name = forms.CharField(label=_(u'Last Name'), max_length=30)
    username = forms.CharField(label=_(u'Username'), max_length=30)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['username'].initial = self.instance.user.username

    def save(self, *args, **kwargs):
        super(UserProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('first_name')
        self.instance.user.last_name = self.cleaned_data.get('last_name')
        self.instance.user.username = self.cleaned_data.get('username')
        self.instance.user.save()

    class Meta:
        model = UserProfile
        exclude = ('user', 'moh_facility', 'level',)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
