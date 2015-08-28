from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import Patient
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable

def home(request):
    return render(request, 'base_layout.html')

@login_required
def statistics(request):
    datum = None
    formset = SearchForm()
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        formset = SearchForm(request.POST)
        if formset.is_valid() :
            datum = formset.cleaned_data
            if datum['cds']:
                results = PatientTable(Patient.objects.filter(date__range=[datum['start_date'], datum['end_date']], ))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', {'results' : results})

    all_patients = PatientTable(Patient.objects.all())
    RequestConfig(request, paginate={"per_page":25}).configure(all_patients)
    return render(request, 'statistics.html', {'form' : formset, 'all_patients':all_patients })