from django import forms
from surveillance_cholera.models import *


class SearchForm(forms.Form):
    def __init__(self,  request=None, *args, **kwargs):
        user = None
        super (SearchForm,self).__init__( *args,**kwargs)
        PROVINCES = Province.objects.values_list('id','name').distinct()
        if request != None:
            user = UserProfile.objects.get(user=request.user)
            level = user.level
            moh_facility = user.moh_facility

            if level == 'BPS':
                PROVINCES= Province.objects.filter(code=moh_facility).values_list('id','name').distinct()
            if level=='BDS':
                district = District.objects.get(code=moh_facility)
                PROVINCES = Province.objects.filter(code=district.province).values_list('id','name').distinct()
            if level=='CDS':
                cds= CDS.objects.get(code=moh_facility)
                PROVINCES = Province.objects.filter(code=cds.district.province).values_list('id','name').distinct()
        self.base_fields['province'] =  forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')] + [(str(i),n) for i,n in PROVINCES])


    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    cds = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')], required=False)
    districts = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')],  required=False)




    # def clean(self, *args, **kwargs):

    #     start_date = None
    #     end_date = None
    #     cleaned_data = super(SearchForm, self).clean()
    #     try:
    #         start_date = cleaned_data['start_date'][0]
    #     except KeyError:
    #         cleaned_data['end_date'] = date.today()
    #     try:
    #         end_date = cleaned_data['end_date'][0]
    #     except KeyError:
    #         cleaned_data['end_date'] = date.today()

    #     if start_date and start_date > date.today():
    #         self.add_error('start_date',_("The Start Date should not be a date in the future."))
    #     if end_date and start_date and end_date <= start_date:
    #         self.add_error('end_date',_("The End Date should be a date after the Start Date"))
    #     return True