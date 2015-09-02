from django import forms
from surveillance_cholera.models import *


class SearchForm(forms.Form):
    def __init__(self,  request=None, *args, **kwargs):
        user = None
        super (SearchForm,self).__init__( *args,**kwargs)
        PROVINCES = Province.objects.values_list('id','name').distinct()
        if request != None and request.user.is_authenticated():
            user = UserProfile.objects.get(user=request.user)
            level = user.level
            moh_facility = user.moh_facility
            if level == 'BPS':
                PROVINCES= Province.objects.filter(code=moh_facility).values_list('id','name').distinct()
                DISTRICTS = District.objects.filter(province__code=moh_facility).values_list('id','name').distinct()
                CDSS = CDS.objects.filter(district__province__code=moh_facility).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices= [('', '---------')] +[(str(i),n) for i,n in DISTRICTS],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices= [('', '---------')], required=False)

            if level=='BDS':
                district = District.objects.get(code=moh_facility)
                PROVINCES = Province.objects.filter(code=district.province.id).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(district.id), district.name)],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')], required=False)

            if level=='CDS':
                cds= CDS.objects.get(code=moh_facility)
                PROVINCES = Province.objects.filter(code=cds.district.province.id).values_list('id','name').distinct()
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(cds.district.id), cds.district.name)],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[(str(cds.id), cds.name)], required=False)

            if level=='CEN':
                PROVINCES = [('', '---------')] + [(str(i),n) for i,n in PROVINCES]
                self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=PROVINCES)
                self.base_fields['districts'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')],  required=False)
                self.base_fields['cds'] = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')], required=False)


    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
