from django.views.generic import ListView
from surveillance_cholera.models import CDS, Province, District, Patient, Report

class CDSListView(ListView):
    model = CDS
    paginate_by = 10  #and that's it !!

class ProvinceListView(ListView):
    model = Province
    paginate_by = 10  #and that's it !!

class DistrictListView(ListView):
    model = District
    paginate_by = 10  #and that's it !!

class PatientListView(ListView):
    model = Patient
    paginate_by = 10  #and that's it !!

class ReportListView(ListView):
    model = Report
    paginate_by = 10  #and that's it !!