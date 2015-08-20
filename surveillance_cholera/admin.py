from django.contrib import admin

from surveillance_cholera.models import Province, District, CDS

admin.site.register(Province)
admin.site.register(District)
admin.site.register(CDS)
