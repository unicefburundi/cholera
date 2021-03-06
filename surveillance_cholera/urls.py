from django.conf.urls import patterns, url
from surveillance_cholera.backend import handel_rapidpro_request
from surveillance_cholera.views import *
from surveillance_cholera.tasks import ask_update_on_patient

urlpatterns = patterns(
    "",
    # dashboard view for viewing all poll reports in one place
    url(r"external_request", handel_rapidpro_request, name="handel_request"),
    url(r"test_task", ask_update_on_patient, name="test_task"),
    # CDS
    url(r"^cds/$", CDSListView.as_view(), name="cds_list"),
    url(r"^cds/add/$", CDSCreateView.as_view(), name="cds_add"),
    url(r"^cds/(?P<pk>\d+)/$", CDSDetailView.as_view(), name="cds_detail"),
    url(r"^cds_statistics/(?P<pk>\d+)/$", CDSFormView.as_view(), name="cds_statistics"),
    # Districts
    url(r"^district/$", DistrictListView.as_view(), name="district_list"),
    url(r"^district/add/$", DistrictCreateView.as_view(), name="district_add"),
    url(
        r"^district/(?P<pk>\d+)/$", DistrictDetailView.as_view(), name="district_detail"
    ),
    url(
        r"^district_statistics/(?P<pk>\d+)/$",
        DistrictFormView.as_view(),
        name="district_statistics",
    ),
    # Provinces
    url(r"^province/$", ProvinceListView.as_view(), name="province_list"),
    url(r"^province/add/$", ProvinceCreateView.as_view(), name="province_add"),
    url(
        r"^province/(?P<pk>\d+)/$", ProvinceDetailView.as_view(), name="province_detail"
    ),
    url(
        r"^province_statistics/(?P<pk>\d+)/$",
        ProvinceFormView.as_view(),
        name="province_statistics",
    ),
    # Patients
    url(r"^patient/$", PatientListView.as_view(), name="patient_list"),
    url(r"^patient/(?P<pk>\d+)/$", PatientDetailView.as_view(), name="patient_detail"),
    url(
        r"^patients/(?P<code>\d+)/$", get_patients_by_code, name="get_patients_by_code"
    ),
    # Alerts
    url(r"^get_alerts/$", get_alerts, name="get_alerts"),
    # moh_facility
    url(r"^moh_facility/$", moh_facility, name="moh_facility"),
    # ProfileUser
    url(r"^register/$", UserSignupView.as_view(), name="create_profile"),
    url(
        r"^profile/(?P<pk>\d+)/$",
        ProfileUserDetailView.as_view(),
        name="profile_user_detail",
    ),
    url(
        r"^profile_edit/(?P<pk>\d+)/$",
        ProfileUserUpdateView.as_view(),
        name="profileuser_update",
    ),
)
