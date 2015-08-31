from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient, Report
from authentication.models import UserProfile


class CDSListView(ListView):
    model = CDS
    paginate_by = 25

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        qs = CDS.objects.all()
        user = UserProfile.objects.get(user=self.request.user.id)
        if user.level == 'CDS':
            qs = CDS.objects.filter(code=int(user.moh_facility))
        if user.level == 'BSD':
            qs = CDS.objects.filter(district=int(user.moh_facility))
        if user.level == 'BPS':
            qs = CDS.objects.filter(district__province=int(user.moh_facility))
        return qs


class CDSDetailView(DetailView):
    model = CDS

    def get_context_data(self, **kwargs):
        context = super(CDSDetailView, self).get_context_data(**kwargs)
        city = Patient.objects.filter(cds=self.kwargs['pk'])
        context['patients'] = city
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
        if user.level == 'BSD':
            qs = District.objects.filter(code=int(user.moh_facility))
        if user.level == 'BPS':
            qs = District.objects.filter(province=int(user.moh_facility))
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
            qs = Patient.objects.filter(cds=int(user.moh_facility))
        if user.level == 'BSD':
            qs = Patient.objects.filter(cds__district=int(user.moh_facility))
        if user.level == 'BPS':
            qs = Patient.objects.filter(cds__district__province=int(user.moh_facility))
        return qs

class PatientDetailView(DetailView):
    model = Patient

class ReportListView(ListView):
    model = Report
    paginate_by = 25

class ReportDetailView(DetailView):
    model = Report