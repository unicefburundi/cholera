from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'cholera.views.home', name='home'),
    url(r'^landing/$', 'cholera.views.landing', name='landing'),
    url(r'^get_cdss/(?P<district_id>\d+)/$', 'cholera.views.get_cdss', name="get_cdss"),
    url(r'^get_districts/(?P<province_id>\d+)/$', 'cholera.views.get_districts', name="get_districts"),
    url(r'^get_by_code/(?P<code>\d+)/$', 'cholera.views.get_by_code', name="get_by_code"),
    url(r'^search_patients/$', 'cholera.views.search_patients', name='search_patients'),
    url(r'^get_statistics/$', 'cholera.views.get_statistics', name='get_statistics'),
    url(r'^get_by_level/(?P<level>\w+)/$', 'cholera.views.get_by_level', name='get_by_level'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('authentication.urls')),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^cholera/', include('surveillance_cholera.urls')),
) +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
