from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient, Report
from authentication.models import UserProfile
from django_tables2 import  RequestConfig
from surveillance_cholera.tables import PatientsTable, Patients2Table
from django.shortcuts import render
from surveillance_cholera.forms import PatientSearchForm, SearchForm
from django.contrib.auth.decorators import login_required
from surveillance_cholera.tables import PatientTable, ReportTable
from cholera.views import get_all_patients
from django.db.models import Q
import datetime
from django.views.generic import FormView
from surveillance_cholera.templatetags.extras_utils import format_to_time, DEAD, HOSPI, SORTI
import operator

###########
# CDS             ##
###########

def get_per_cds_statistics(moh_facility_id, start_date='', end_date=''):
    if start_date == '':
        start_date = u'01/01/2012'
    if end_date == '':
        end_date = datetime.date.today().strftime('%d/%m/%Y')
    patients = Patient.objects.filter(date_entry__range=[format_to_time(start_date), format_to_time(end_date)]).filter(cds=moh_facility_id)
    facility = {'name': CDS.objects.get(id=moh_facility_id).name}
    detail = {'detail':  CDS.objects.get(id=moh_facility_id).code}
    total ={'total': patients.count()}
    deces= {'deces' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in DEAD)).count()}
    sorties = {'sorties' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in SORTI)).count()}
    hospi = {'hospi' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in HOSPI)).count()}
    nc = {'nc' : patients.filter(exit_status=None).count()}

    elemet = {}
    for i in [total,deces,sorties,hospi,nc, facility, detail]:
            elemet.update(i)
    return elemet



class CDSListView(ListView):
    model = CDS
    paginate_by = 25

class CDSDetailView(DetailView):
    model = CDS


    def get_context_data(self, *args, **kwargs):
        context = super(CDSDetailView, self).get_context_data(*args, **kwargs)
        cds_id = self.kwargs['pk']
        data = [get_per_cds_statistics(cds_id)]
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        context['form'] = SearchForm()
        self.request.session['sstart_date'] = ''
        self.request.session['eend_date'] = ''
        return context

class CDSFormView(FormView, CDSDetailView):
    models = CDS
    form_class = SearchForm
    template_name = 'surveillance_cholera/cds_detail.html'

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = [get_per_cds_statistics(kwargs['pk'], request.POST.get('start_date'), request.POST.get('end_date'))]
        statistics = PatientsTable(data)
        RequestConfig(request).configure(statistics)
        request.session['sstart_date'] = request.POST.get('start_date')
        request.session['eend_date'] = request.POST.get('end_date')

        return render(request, 'surveillance_cholera/cds_detail.html', {'form':form, 'statistics':statistics, 'object': CDS.objects.get(pk=kwargs['pk']),'start_date': request.POST.get('start_date'), 'end_date':request.POST.get('end_date')} )


###########
# District        ##
###########

def get_per_district_statistics(moh_facility_id, start_date='', end_date=''):
    if start_date == '':
        start_date = u'01/01/2012'
    if end_date == '':
        end_date = datetime.date.today().strftime('%d/%m/%Y')
    patients = Patient.objects.filter(date_entry__range=[format_to_time(start_date), format_to_time(end_date)]).filter(cds__district=moh_facility_id)
    facility = {'name': District.objects.get(id=moh_facility_id).name}
    detail = {'detail':  District.objects.get(id=moh_facility_id).code}
    total ={'total': patients.count()}
    deces= {'deces' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in DEAD)).count()}
    sorties = {'sorties' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in SORTI)).count()}
    hospi = {'hospi' : reduce(operator.or_, (patients.filter(intervention__icontains=item) for item in HOSPI)).count()}
    nc = {'nc' : patients.filter(exit_status=None).count()}

    elemet = {}
    for i in [total,deces,sorties,hospi,nc, facility, detail]:
            elemet.update(i)
    return elemet

def get_district_data(moh_facility_id, start_date='', end_date=''):
    elemet = []
    for i in CDS.objects.filter(district=moh_facility_id):
        elemet.append(get_per_cds_statistics(i.id, start_date, end_date))
    return elemet

class DistrictListView(ListView):
    model = District
    paginate_by = 25

class DistrictDetailView(DetailView):
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        district_id = self.kwargs['pk']
        data = get_district_data(district_id)
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        context['form'] = SearchForm()
        self.request.session['sstart_date'] = ''
        self.request.session['eend_date'] = ''
        return context

class DistrictFormView(FormView, DistrictDetailView):
    models = District
    form_class = SearchForm
    template_name = 'surveillance_cholera/district_detail.html'

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = get_district_data(kwargs['pk'], request.POST.get('start_date'), request.POST.get('end_date'))
        statistics = PatientsTable(data)
        RequestConfig(request).configure(statistics)
        request.session['sstart_date'] = request.POST.get('start_date')
        request.session['eend_date'] = request.POST.get('end_date')

        return render(request, 'surveillance_cholera/district_detail.html', {'form':form, 'statistics':statistics, 'object': District.objects.get(pk=kwargs['pk']), 'start_date': request.POST.get('start_date'), 'end_date':request.POST.get('end_date')} )

###########
# Province      ##
###########

def get_province_data(moh_facility_id, start_date='', end_date=''):
    elemet = []
    for i in District.objects.filter(province=moh_facility_id):
        elemet.append(get_per_district_statistics(i.id, start_date, end_date))
    return elemet

class ProvinceListView(ListView):
    model = Province
    paginate_by = 25


class ProvinceDetailView(DetailView):
    model = Province

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        province_id = self.kwargs['pk']
        data = get_province_data(province_id)
        statistics = Patients2Table(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        context['form'] = SearchForm()
        self.request.session['sstart_date'] = ''
        self.request.session['eend_date'] = ''
        return context


###########
# Patient        ##
###########

class PatientListView(ListView):
    model = Patient
    paginate_by = 25

    def get_queryset(self):
        qs = Patient.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == 'CDS':
            qs = Patient.objects.filter(cds__code=int(user.moh_facility))
        if user.level == 'BDS':
            qs = Patient.objects.filter(cds__district__code=int(user.moh_facility))
        if user.level == 'BPS':
            qs = Patient.objects.filter(cds__district__province__code=int(user.moh_facility))
        return qs

class PatientDetailView(DetailView):
    model = Patient

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        patient_id = self.kwargs['pk']
        data = Report.objects.filter(patient__id=patient_id)
        reports = ReportTable(data)
        RequestConfig(self.request).configure(reports)
        context['reports'] = reports
        return context

@login_required
def get_patients_by_code(request, code=''):
    userprofile = UserProfile.objects.get(user=request.user)
    all_patients = get_all_patients(level=userprofile.level, moh_facility=userprofile.moh_facility)
    form = PatientSearchForm()
    moh_facility = None
    if len(code)<=2 :
        moh_facility = Province.objects.get(code=code)
        all_patients = all_patients.filter(cds__district__province__code=code)
    if len(code)>2 and len(code)<=4 :
        moh_facility = District.objects.get(code=code)
        all_patients = all_patients.filter(cds__district__code=code)
    if len(code)>4 :
        moh_facility = CDS.objects.get(code=code)
        all_patients = all_patients.filter(cds__code=code)
    sstart_date = request.session['sstart_date']
    eend_date = request.session['eend_date']
    if sstart_date == None or sstart_date == '':
        sstart_date= datetime.date(2012,1,1).strftime('%d/%m/%Y')
    if eend_date == None or eend_date == '':
        eend_date = datetime.date.today().strftime('%d/%m/%Y')
    all_patients = all_patients.filter(date_entry__range=[format_to_time(sstart_date), format_to_time(eend_date)])

    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['intervention'] !='':
                all_patients = all_patients.filter(Q(intervention=form.cleaned_data['intervention']))
            if form.cleaned_data['sexe'] !='':
                all_patients = all_patients.filter(Q(sexe=form.cleaned_data['sexe']))
            if form.cleaned_data['age'] !='':
                all_patients = all_patients.filter(Q(age=form.cleaned_data['age']))
            if form.cleaned_data['colline_name'] !='':
                all_patients = all_patients.filter(Q(colline_name__icontains=form.cleaned_data['colline_name']))
            if form.cleaned_data['exit_status'] !='':
                all_patients = all_patients.filter(Q(exit_status=form.cleaned_data['exit_status']))
            if form.cleaned_data['start_date'] == None:
                form.cleaned_data['start_date']= datetime.date(2012,1,1)
            if form.cleaned_data['end_date'] == None:
                form.cleaned_data['end_date'] = datetime.date.today()

            results = PatientTable(all_patients.filter(date_entry__range=[form.cleaned_data['start_date'], form.cleaned_data['end_date']]))
            RequestConfig(request, paginate={"per_page": 25}).configure(results)
            return render(request, 'surveillance_cholera/patients.html', { 'form':form, 'results' : results, 'moh_facility': moh_facility, 'sstart_date':request.session['sstart_date'], 'eend_date':request.session['eend_date']})


    results = PatientTable(all_patients)
    RequestConfig(request, paginate={"per_page": 25}).configure(results)
    return render(request, 'surveillance_cholera/patients.html', { 'form':form, 'results' : results, 'moh_facility': moh_facility, 'sstart_date':request.session['sstart_date'], 'eend_date':request.session['eend_date']})


class ProvinceFormView(FormView, ProvinceDetailView):
    models = Province
    form_class = SearchForm
    template_name = 'surveillance_cholera/province_detail.html'

    def post(self, request, *args, **kwargs):
        form = SearchForm(request)
        data = get_province_data(kwargs['pk'], request.POST.get('start_date'), request.POST.get('end_date'))
        statistics = Patients2Table(data)
        RequestConfig(request).configure(statistics)
        request.session['sstart_date'] = request.POST.get('start_date')
        request.session['eend_date'] = request.POST.get('end_date')

        return render(request, 'surveillance_cholera/province_detail.html', {'form':form, 'statistics':statistics, 'object': Province.objects.get(pk=kwargs['pk']), 'start_date': request.POST.get('start_date'), 'end_date':request.POST.get('end_date')} )