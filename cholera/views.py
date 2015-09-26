from django.shortcuts import render
from surveillance_cholera.forms import SearchForm
from surveillance_cholera.models import CDS,District, Province, Patient
from django_tables2   import RequestConfig
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable, Patients3Table
from django.http import JsonResponse
import datetime
from surveillance_cholera.templatetags.extras_utils import format_to_time, get_all_patients, DEAD, HOSPI, SORTI
from authentication.models import UserProfile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import operator

def get_province_statistics(province, start_date='', end_date=''):
    elemet = {}
    facility = {'name': province.name}
    detail = {'detail':  province.id}
    patients = Patient.objects.filter(date_entry__range=[start_date, end_date]).filter(cds__district__province=province.id)
    total ={'total': Patient.objects.filter(cds__district__province=province.id).count()}
    deces= {'deces' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in DEAD)).count()}
    sorties = {'sorties' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in SORTI)).count()}
    hospi = {'hospi' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in HOSPI)).count()}
    nc = {'nc' : patients.count()}

    for i in [total,deces,sorties,hospi,nc, facility, detail]:
        elemet.update(i)

    return elemet

def home(request):
    return render(request, 'landing_page.html')

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


@login_required
def search_patients(request):
    return get_statistics(request)


@login_required
def get_statistics(request):
    form = SearchForm(request)
    userprofile = UserProfile.objects.get(user=request.user)
    all_patients = get_all_patients(level=userprofile.level, moh_facility=userprofile.moh_facility)

    if request.method == 'POST':
        if request.POST.get('patient') !='':
            all_patients = all_patients.filter(patient_id__icontains=request.POST.get('patient'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if request.POST.get('start_date') == '':
            start_date = u'01/01/2012'
        if request.POST.get('end_date') == '':
            end_date = datetime.date.today().strftime('%d/%m/%Y')
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

def get_by_code(request, code='', start_date='', end_date=''):
    request.session['sstart_date'] = start_date
    request.session['eend_date'] = end_date
    if code=='None':
        form = SearchForm
        results = [get_province_statistics(i, format_to_time(start_date), format_to_time(end_date)) for i in Province.objects.all() ]
        statistics = Patients3Table(results)
        RequestConfig(request, paginate={"per_page": 25}).configure(statistics)
        request.session['sstart_date'] = request.POST.get('start_date')
        request.session['eend_date'] = request.POST.get('end_date')
        return render(request, 'surveillance_cholera/provinces.html', {  'statistics' : statistics, 'form':form, 'start_date':request.POST.get('start_date'), 'end_date':request.POST.get('end_date')})
    if len(code)<=2 :
        url = reverse('province_detail', kwargs={'pk': Province.objects.get(code=code).id})
        return HttpResponseRedirect(url)
    if len(code)>2 and len(code)<=4 :
        url = reverse('district_detail', kwargs={'pk': District.objects.get(code=str(code)).id})
        return HttpResponseRedirect(url)
    if len(code)>4 :
        url = reverse('cds_detail', kwargs={'pk': CDS.objects.get(code=code).id})
        return HttpResponseRedirect(url)

def landing(request):
    code = UserProfile.objects.get(user=request.user).moh_facility
    start_date = u'01/01/2012'
    end_date = datetime.date.today().strftime('%d/%m/%Y')
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if request.POST.get('start_date') == '':
            start_date = u'01/01/2012'
        if request.POST.get('end_date') == '':
            end_date = datetime.date.today().strftime('%d/%m/%Y')

    return get_by_code(request=request,code=str(code), start_date=start_date, end_date=end_date)
