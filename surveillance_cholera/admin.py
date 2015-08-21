from django.contrib import admin

from surveillance_cholera.models import Province, District, CDS, Reporter, Temporary

admin.site.register(Province)
admin.site.register(District)
admin.site.register(CDS)
admin.site.register(Reporter)
admin.site.register(Temporary)
