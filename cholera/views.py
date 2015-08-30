from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import Patient, CDS,District, Province
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable
from django.http import JsonResponse
from django.http import HttpResponse


def home(request):
    return render(request, 'base_layout.html')

def get_cdss(request, district_id):
    opt2_html = ""
    try:
        district = District.objects.get(pk=district_id)
        cdss = CDS.objects.filter(district=district)
        for cds in cdss:
            opt2_html += "<option value='"+str(cds.id)+"'>"+cds.name+"</option>"
    except:
        print "Error in fetching options 2"
    return HttpResponse(opt2_html)

def get_districts(request, province_id):
    opt2_html = ""
    try:
        province = Province.objects.get(pk=province_id)
        districts = District.objects.filter(province=province)
        for district in districts:
            opt2_html += "<option value='"+str(district.id)+"'>"+district.name+"</option>"
    except:
        print "Error in fetching options 2"
    return HttpResponse(opt2_html)

@login_required
def statistics(request):
    datum = None
    formset = SearchForm()
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        formset = SearchForm(request.POST)
        if formset.is_valid() :
            datum = formset.cleaned_data
            if datum['cds']:
                results = PatientTable(Patient.objects.filter(date__range=[datum['start_date'], datum['end_date']], ))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', {'results' : results})

    all_patients = PatientTable(Patient.objects.all())
    provinces = Province.objects.all()
    RequestConfig(request, paginate={"per_page":25}).configure(all_patients)
    return render(request, 'statistics.html', {'form' : formset, 'all_patients':all_patients, 'provinces':provinces })

