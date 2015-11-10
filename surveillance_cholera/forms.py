from django import forms
from surveillance_cholera.models import *
from authtools.forms import UserCreationForm
from betterforms.multiform import MultiModelForm
from collections import OrderedDict

class SearchForm(forms.Form):
    def __init__(self,  request=None, *args, **kwargs):
        user = None
        PROVINCES = Province.objects.values_list('id','name').distinct()
        import ipdb; ipdb.set_trace()
        if request and request.user.is_authenticated():
            user = UserProfile.objects.get_or_create(user=request.user)
            level = user[0].level
            moh_facility = user[0].moh_facility
            if level == 'BPS':
                PROVINCES= Province.objects.filter(code=moh_facility).values_list('id','name').distinct()
                DISTRICTS = District.objects.filter(province__code=moh_facility).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices= [('', '---------')] +[(str(i),n) for i,n in DISTRICTS],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices= [('', '---------')], required=False)

            if level=='BDS':
                district = District.objects.get(code=moh_facility)
                CDSS = CDS.objects.filter(district=district).values_list('id','name').distinct()
                PROVINCES = Province.objects.filter(code=district.province.id).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(district.id), district.name)],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')]+[(str(i),n) for i,n in CDSS], required=False)

            if level=='CDS':
                cds= CDS.objects.get(code=moh_facility)
                PROVINCES = Province.objects.filter(code=cds.district.province.id).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(cds.district.id), cds.district.name)],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(cds.id), cds.name)], required=False)

            if level in ['CEN', 'Central']:
                PROVINCES = [('', '---------')] + [(str(i),n) for i,n in PROVINCES]
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')], required=False)
        super (SearchForm,self).__init__( *args,**kwargs)


    start_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'class':'datePicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    patient = forms.CharField()

    class Meta:
        widgets = {
            'patient': forms.TextInput(attrs={'placeholder': 'What\'s your name?'}),
        }


class PatientSearchForm(forms.ModelForm):
    start_date = forms.DateField( widget=forms.TextInput(attrs={'class':'datePicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    exit_status = forms.ChoiceField(widget = forms.Select(), choices=[('','-----'),('Pr', 'Reference'), ('Pd', 'Deces'), ('Pg', 'Gueris')])
    sexe = forms.ChoiceField(widget = forms.Select(), choices=[('','-----'),('M', 'Male'), ('F', 'Female')])
    intervention = forms.ChoiceField(widget = forms.Select(), choices=[('','-----'),('HOSPI', 'Hospitalisation'), ('DD', 'Deces'), ('PR', 'Reference'), ('DESH', 'Non Hospitalise')])
    age = forms.ChoiceField(widget = forms.Select(), choices=[('','-----'),('A1', 'Inf 5ans'), ('A2', 'Sup 5ans')])

    def __init__(self, *args, **kwargs):
        super(PatientSearchForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Patient
        exclude = ('patient_id','date_entry', 'exit_date', 'cds')

class AlertForm(forms.Form):
    """docstring for AlertForm"""
    treshold = forms.IntegerField(initial=3, required=False)

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    province = forms.ModelChoiceField(queryset=Province.objects.order_by('name'))
    class Meta:
        model = District
        fields = '__all__'

class CDSForm(forms.ModelForm):
    class Meta:
        model = CDS
        fields = '__all__'

#User
class UserCreationForm(UserCreationForm):
    """
    A UserCreationForm with optional password inputs.
    """

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

class UserProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict((
        ('user', UserCreationForm),
        ('profile', UserProfileForm2),
    ))
