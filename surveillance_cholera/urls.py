from django.conf.urls import *
from surveillance_cholera.backend import handel_rapidpro_request
from .views import *

urlpatterns = patterns('',
    # dashboard view for viewing all poll reports in one place
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^cds/$', CDSListView.as_view(), name='cds_list'),
    url(r'^cds/(?P<pk>\d+)/$', CDSDetailView.as_view(), name='cds_detail'),
    url(r'^district/', DistrictListView.as_view(), name='district_list'),
    url(r'^province/', ProvinceListView.as_view(), name='province_list'),
    url(r'^patient/', PatientListView.as_view(), name='patient_list'),
    url(r'^report/', ReportListView.as_view(), name='report_list')

)