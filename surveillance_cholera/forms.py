from django import forms
from django.utils.translation import ugettext as _
from surveillance_cholera.models import *
from datetime import date


class SearchForm(forms.Form):
    PROVINCES = Province.objects.values_list('id','name').distinct()
    province = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')] + [(str(i),n) for i,n in PROVINCES])
    districts = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')],  required=False)
    cds = forms.ChoiceField(widget = forms.Select(), choices=[('', '---------')], required=False)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'class':'datePicker'}))

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