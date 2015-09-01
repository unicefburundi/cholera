from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient, Report
from authentication.models import UserProfile
import django_tables2 as tables
from django_tables2 import  RequestConfig

###########
# CDS              ##
###########

def get_data(moh_facility):
    total ={'total': Patient.objects.filter(cds=moh_facility).count()}
    deces= {'deces' : Patient.objects.filter(cds=moh_facility, intervention='DD').count()}
    sorties = {'sorties' : Patient.objects.filter(cds=moh_facility, intervention='PR').count()}
    hospi = {'hospi' : Patient.objects.filter(cds=moh_facility, intervention='HOSPI').count()}
    nc = {'nc' : Patient.objects.filter(cds=moh_facility, exit_status=None).count()}

    elemet = {}
    for i in [total,deces,sorties,hospi,nc]:
            elemet.update(i)
    return [elemet]

class PatientTable(tables.Table):
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()

    class Meta:
        attrs = {"class": "table table-bordered table-hover"}


class CDSListView(ListView):
    model = CDS
    paginate_by = 25

    def get_queryset(self):
        qs = CDS.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == 'CDS':
            qs = CDS.objects.filter(code=int(user.moh_facility))
        if user.level == 'BDS':
            qs = CDS.objects.filter(district__code=int(user.moh_facility))
        if user.level == 'BPS':
            qs = CDS.objects.filter(district__province__code=int(user.moh_facility))
        return qs


class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, **kwargs):
        context = super(CDSDetailView, self).get_context_data(**kwargs)
        moh_facility = self.kwargs['pk']
        patients = Patient.objects.filter(cds=moh_facility)
        context['patients'] = patients
        data = get_data(moh_facility)
        table = PatientTable(data)
        RequestConfig(self.request).configure(table)
        context['table'] = table
        return context

class ProvinceListView(ListView):
    model = Province
    paginate_by = 25

    def get_queryset(self):
        qs = Province.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == 'BPS':
            qs = Province.objects.filter(code=int(user.moh_facility))
        return qs

class ProvinceDetailView(DetailView):
    model = Province

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        districts = District.objects.filter(province=self.kwargs['pk'])
        context['districts'] = districts
        return context

class DistrictListView(ListView):
    model = District
    paginate_by = 25

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        qs = District.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == 'BDS':
            qs = District.objects.filter(code=int(user.moh_facility))
        if user.level == 'BPS':
            qs = District.objects.filter(province__code=int(user.moh_facility))
        return qs


class DistrictDetailView(DetailView):
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        cdss = CDS.objects.filter(district=self.kwargs['pk'])
        context['cdss'] = cdss
        return context

class PatientListView(ListView):
    model = Patient
    paginate_by = 25

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
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

class ReportListView(ListView):
    model = Report
    paginate_by = 25

class ReportDetailView(DetailView):
    model = Report