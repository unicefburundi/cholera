from django.views.generic import ListView, DetailView
from surveillance_cholera.models import CDS, Province, District, Patient, Report

class CDSListView(ListView):
    model = CDS
    paginate_by = 10

class CDSDetailView(DetailView):
    model = CDS



class ProvinceListView(ListView):
    model = Province
    paginate_by = 10

class DistrictListView(ListView):
    model = District
    paginate_by = 10

class PatientListView(ListView):
    model = Patient
    paginate_by = 10

class ReportListView(ListView):
    model = Report
    paginate_by = 10