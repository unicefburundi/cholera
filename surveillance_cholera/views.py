from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient
from authentication.models import UserProfile
from django_tables2 import  RequestConfig
from surveillance_cholera.tables import PatientsTable

###########
# CDS              ##
###########

def get_per_cds_data(moh_facility):
    facility = {'name': CDS.objects.get(id=moh_facility).name}
    total ={'total': Patient.objects.filter(cds=moh_facility).count()}
    deces= {'deces' : Patient.objects.filter(cds=moh_facility, intervention='DD').count()}
    sorties = {'sorties' : Patient.objects.filter(cds=moh_facility, intervention='PR').count()}
    hospi = {'hospi' : Patient.objects.filter(cds=moh_facility, intervention='HOSPI').count()}
    nc = {'nc' : Patient.objects.filter(cds=moh_facility, exit_status=None).count()}

    elemet = {}
    for i in [total,deces,sorties,hospi,nc, facility]:
            elemet.update(i)
    return elemet

def get_per_district_data(moh_facility):
    facility = {'name': District.objects.get(id=moh_facility).name}
    total ={'total': Patient.objects.filter(cds__district=moh_facility).count()}
    deces= {'deces' : Patient.objects.filter(cds__district=moh_facility, intervention='DD').count()}
    sorties = {'sorties' : Patient.objects.filter(cds__district=moh_facility, intervention='PR').count()}
    hospi = {'hospi' : Patient.objects.filter(cds__district=moh_facility, intervention='HOSPI').count()}
    nc = {'nc' : Patient.objects.filter(cds__district=moh_facility, exit_status=None).count()}

    elemet = {}
    for i in [total,deces,sorties,hospi,nc, facility]:
            elemet.update(i)
    return elemet

def get_district_data(moh_facility):
    elemet = []
    for i in CDS.objects.filter(district=moh_facility):
        elemet.append(get_per_cds_data(i.id))
    return elemet

def get_province_data(moh_facility):
    elemet = []
    for i in District.objects.filter(province=moh_facility):
        elemet.append(get_per_district_data(i.id))
    return elemet




class CDSListView(ListView):
    model = CDS
    paginate_by = 25



class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, **kwargs):
        context = super(CDSDetailView, self).get_context_data(**kwargs)
        moh_facility = self.kwargs['pk']
        patients = Patient.objects.filter(cds=moh_facility)
        context['patients'] = patients
        data = [get_per_cds_data(moh_facility)]
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        return context

class ProvinceListView(ListView):
    model = Province
    paginate_by = 25


class ProvinceDetailView(DetailView):
    model = Province

    def get_context_data(self, **kwargs):
        context = super(ProvinceDetailView, self).get_context_data(**kwargs)
        moh_facility = self.kwargs['pk']
        districts = District.objects.filter(province=moh_facility)
        context['districts'] = districts
        data = get_province_data(moh_facility)
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        return context

class DistrictListView(ListView):
    model = District
    paginate_by = 25



class DistrictDetailView(DetailView):
    model = District

    def get_context_data(self, **kwargs):
        context = super(DistrictDetailView, self).get_context_data(**kwargs)
        moh_facility = self.kwargs['pk']
        cdss = CDS.objects.filter(district=moh_facility)
        context['cdss'] = cdss
        data = get_district_data(moh_facility)
        statistics = PatientsTable(data)
        RequestConfig(self.request).configure(statistics)
        context['statistics'] = statistics
        return context

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
