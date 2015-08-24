from django.conf.urls import *
from surveillance_cholera.backend import handel_rapidpro_request
from .views import *

urlpatterns = patterns('',
    # dashboard view for viewing all poll reports in one place
    url(r'external_request', handel_rapidpro_request, name="handel_request"),
    url(r'^person/', PersonListView.as_view(), name='person_list')
)