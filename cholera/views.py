from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import Patient, CDS,District, Province
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable
from django.http import JsonResponse
import datetime
from surveillance_cholera.templatetags.extras_utils import format_to_time
from authentication.models import UserProfile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

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
    province = Province.objects.get(pk=province_id)
    districts = District.objects.filter(province=province)
    districts_dict = {}
    for district in districts:
        districts_dict[district.id] = district.name
    return JsonResponse([districts_dict], safe=False)

def get_all_patients(level=None,moh_facility=None):
    if level=='CDS':
        return Patient.objects.filter(cds__code=moh_facility)
    if level=='BDS':
        return Patient.objects.filter(cds__district__code=moh_facility)
    if level =='BPS':
        return Patient.objects.filter(cds__district__province__code=moh_facility)
    else:
        return Patient.objects.all()

@login_required
def statistics(request):
    return get_statistics(request)


@login_required
def get_statistics(request):
    form = SearchForm(request)
    userprofile = UserProfile.objects.get(user=request.user)
    all_patients = get_all_patients(level=userprofile.level, moh_facility=userprofile.moh_facility)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if request.POST.get('start_date') == '':
            start_date = u'01/01/2012'
        if request.POST.get('end_date') == '':
            end_date = datetime.date.today().strftime('%m/%d/%Y')
        if request.POST.get('province') !='':
            if request.POST.get('districts') != '':
                if request.POST.get('cds') != '':
                    results = PatientTable(all_patients.filter(cds=request.POST.get('cds'), date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
                    RequestConfig(request, paginate={"per_page": 25}).configure(results)
                    return render(request, 'statistics.html', { 'form':form, 'results' : results})
                results = PatientTable(all_patients.filter(cds__district__id=request.POST.get('districts'),date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
                RequestConfig(request, paginate={"per_page": 25}).configure(results)
                return render(request, 'statistics.html', { 'form':form, 'results' : results})
            results = PatientTable(all_patients.filter(cds__district__province__id=request.POST.get('province'),date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
            RequestConfig(request, paginate={"per_page": 25}).configure(results)
            return render(request, 'statistics.html', { 'form':form, 'results' : results})
        results = PatientTable(all_patients.filter(date_entry__range=[format_to_time(start_date), format_to_time(end_date)]))
        RequestConfig(request, paginate={"per_page": 25}).configure(results)
        return render(request, 'statistics.html', { 'form':form, 'results' : results})
    results = PatientTable(all_patients)
    RequestConfig(request, paginate={"per_page": 25}).configure(results)
    return render(request, 'statistics.html', { 'form':form, 'results' : results})

def get_by_code(request, code=''):
    if len(code)<=2 :
        url = reverse('province_detail', kwargs={'pk': Province.objects.get(code=code).id})
        return HttpResponseRedirect(url)
    if len(code)>2 and len(code)<=4 :
        url = reverse('district_detail', kwargs={'pk': District.objects.get(code=code).id})
        return HttpResponseRedirect(url)
    if len(code)>4 :
        url = reverse('cds_detail', kwargs={'pk': CDS.objects.get(code=code).id})
        return HttpResponseRedirect(url)

