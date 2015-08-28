from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'cholera.views.home', name='home'),
    url(r'^statistics/$', 'cholera.views.statistics', name='statistics'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', include('authentication.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^cholera/', include('surveillance_cholera.urls')),
) +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#In development, static files should be served from app static directories
if settings.DEBUG == True:
    urlpatterns += staticfiles_urlpatterns()
