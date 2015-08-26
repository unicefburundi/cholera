from authentication.views import *
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required as auth

urlpatterns = patterns('',
    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^edit_profile/$', auth(UserProfileEditView.as_view()), name="edit_profile"),
    )