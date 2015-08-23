from django.contrib.auth.decorators import login_required as auth
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from authentication.views import UserProfileDetailView, UserProfileEditView

urlpatterns = patterns('',
    url(r'^$', 'cholera.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/(?P<slug>\w+)/$', UserProfileDetailView.as_view(), name="profile"),
    url(r'^edit_profile/$', auth(UserProfileEditView.as_view()), name="edit_profile"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^cholera/', include('surveillance_cholera.urls')),
) +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
