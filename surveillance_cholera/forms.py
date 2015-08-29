from django import forms
from django.utils.translation import ugettext as _
from surveillance_cholera.models import *
from datetime import date

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField) or isinstance(f, models.DateTimeField):
        formfield.widget.format = '%d/%m/%Y'
        formfield.widget.attrs.update({'class':'datePicker form-control', 'readonly':'true'})
    return formfield

class SearchForm(forms.Form):
    PROVINCES = Province.objects.values_list('id','name').distinct()
    # import ipdb; ipdb.set_trace()
    province = forms.ChoiceField(choices=[(str(i),n) for i,n in PROVINCES])
    districts = forms.ChoiceField(choices=[('0', 'All'),])
    cds = forms.ChoiceField(choices=[('0', 'All'),])
    start_date = forms.DateField()
    end_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SearchForm, self).__init__(*args, **kwargs)
        self.formfield_callback = make_custom_datefield

    def clean(self, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        start_date = None
        end_date = None
        cleaned_data = super(SearchForm, self).clean()
        try:
            start_date = cleaned_data['start_date']
        except KeyError:
            cleaned_data['end_date'] = date.today()
        try:
            end_date = cleaned_data['end_date']
        except KeyError:
            cleaned_data['end_date'] = date.today()

        if start_date and start_date > date.today():
            self.add_error('start_date',_("The Start Date should not be a date in the future."))
        if end_date and start_date and end_date <= start_date:
            self.add_error('end_date',_("The End Date should be a date after the Start Date"))

    class Meta:
        model = SearchModel
        exclude = []