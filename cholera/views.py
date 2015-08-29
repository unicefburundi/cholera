from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import Patient, CDS,District, Province
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable
from django.http import JsonResponse


def home(request):
    return render(request, 'base_layout.html')

def get_cdss(request, district_id):
    district = District.objects.get(pk=district_id)
    cdss = CDS.objects.filter(district=district)
    cds_dict = {}
    for cds in cdss:
        cds_dict[cds.id] = cds.name
    return JsonResponse([cds_dict], safe=False)

def get_districts(request, province_id):
    # import ipdb; ipdb.set_trace()
    province = Province.objects.get(pk=province_id)
    districts = District.objects.filter(province=province)
    districts_dict = {}
    for district in districts:
        districts_dict[district.id] = district.name
    return JsonResponse([districts_dict], safe=False)

@login_required
def statistics(request):
    datum = None
    formset = SearchForm()
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        formset = SearchForm(request.POST)
        if formset.is_valid() :
            import ipdb; ipdb.set_trace()
            datum = formset.cleaned_data
            if datum['cds']:
                results = PatientTable(Patient.objects.filter(date__range=[datum['start_date'], datum['end_date']], ))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', {'results' : results})

    all_patients = PatientTable(Patient.objects.all())
    RequestConfig(request, paginate={"per_page":25}).configure(all_patients)
    return render(request, 'statistics.html', {'form' : formset, 'all_patients':all_patients })

