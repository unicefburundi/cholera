from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import Patient, CDS,District, Province
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required, user_passes_test
from surveillance_cholera.tables import PatientTable
from django.http import JsonResponse
import datetime


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
    # import ipdb; ipdb.set_trace()
    if request.method == 'POST':
        formset = SearchForm(request.POST)
        if formset.is_valid() :
            datum = formset.cleaned_data
            if datum['cds']:
                results = PatientTable(Patient.objects.filter(date__range=[datum['start_date'], datum['end_date']] ))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', {'results' : results})

    all_patients = PatientTable(Patient.objects.all())
    RequestConfig(request, paginate={"per_page":25}).configure(all_patients)
    return render(request, 'statistics.html', {'form' : formset, 'all_patients':all_patients })

def format_to_time(date):
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    return d

def not_in_cds_group(user):
    if user:
        return user.groups.filter(name='CDS').count() == 0
    return False

def not_in_bds_group(user):
    if user:
        return user.groups.filter(name='BDS').count() == 0
    return False

def not_in_bps_group(user):
    if user:
        return user.groups.filter(name='BPS').count() == 0
    return False

def not_in_central_group(user):
    if user:
        return user.groups.filter(name='Central').count() == 0
    return False

def get_statistics(request):
    form = SearchForm()
    results = PatientTable(Patient.objects.all())
    if request.method == 'POST':
        # import ipdb; ipdb.set_trace()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if request.POST.get('start_date') == '':
            start_date = u'01/01/2012'
        if request.POST.get('end_date') == '':
            end_date = datetime.date.today().strftime('%m/%d/%Y')
        if request.POST.get('province') !='':
            if request.POST.get('districts') != '':
                if request.POST.get('cds') != '':
                    results = PatientTable(Patient.objects.filter(cds=request.POST.get('cds'), date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
                    RequestConfig(request, paginate={"per_page": 25}).configure(results)
                    return render(request, 'statistics.html', { 'form':form, 'results' : results})
                results = PatientTable(Patient.objects.filter(cds__district=request.POST.get('districts'),date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', { 'form':form, 'results' : results})
            results = PatientTable(Patient.objects.filter(cds__district__province=request.POST.get('province'),date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
            RequestConfig(request, paginate={"per_page": 25}).configure(results)
            return render(request, 'statistics.html', { 'form':form, 'results' : results})
        results = PatientTable(Patient.objects.filter(date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
        RequestConfig(request, paginate={"per_page": 25}).configure(results)
        return render(request, 'statistics.html', { 'form':form, 'results' : results})

    RequestConfig(request, paginate={"per_page": 25}).configure(results)
    return render(request, 'statistics.html', { 'form':form, 'results' : results})