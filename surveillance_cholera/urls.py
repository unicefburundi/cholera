from django.conf.urls import *
from surveillance_cholera.backend import handel_rapidpro_request
from .views import *
from .tasks import *

urlpatterns = patterns('',
    # dashboard view for viewing all poll reports in one place
    url(r'external_request', handel_rapidpro_request, name="handel_request"),

	url(r'test_task', ask_update_on_patient, name="test_task"),

    #CDS
    url(r'^cds/$', CDSListView.as_view(), name='cds_list'),
    url(r'^cds/(?P<pk>\d+)/$', CDSDetailView.as_view(), name='cds_detail'),
    #Districts
    url(r'^district/$', DistrictListView.as_view(), name='district_list'),
    url(r'^district/(?P<pk>\d+)/$', DistrictDetailView.as_view(), name='district_detail'),
    #Provinces
    url(r'^province/$', ProvinceListView.as_view(), name='province_list'),
    url(r'^province/(?P<pk>\d+)/$', ProvinceDetailView.as_view(), name='province_detail'),
    #Patients
    url(r'^patient/$', PatientListView.as_view(), name='patient_list'),
    url(r'^patient/(?P<pk>\d+)/$', PatientDetailView.as_view(), name='patient_detail'),
    #Reports
    url(r'^report/$', ReportListView.as_view(), name='report_list')


)
