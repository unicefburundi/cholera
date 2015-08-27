from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient, Report

class CDSListView(ListView):
    model = CDS
    paginate_by = 25

class CDSDetailView(DetailView):
    model = CDS

class ProvinceListView(ListView):
    model = Province
    paginate_by = 25

class ProvinceDetailView(DetailView):
    model = Province

class DistrictListView(ListView):
    model = District
    paginate_by = 25

class DistrictDetailView(DetailView):
    model = District

class PatientListView(ListView):
    model = Patient
    paginate_by = 25

class PatientDetailView(DetailView):
    model = Patient

class ReportListView(ListView):
    model = Report
    paginate_by = 25

class ReportDetailView(DetailView):
    model = Report