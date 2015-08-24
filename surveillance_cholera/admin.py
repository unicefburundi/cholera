from django.contrib import admin
from surveillance_cholera.models import  *

admin.site.register(Person)
admin.site.register(PhoneNumber)
admin.site.register(Patient)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(CDS)
admin.site.register(Reporter)
admin.site.register(Report)
admin.site.register(TrackPatientMessage)
admin.site.register(GeneralUser)
admin.site.register(ProvinceUser)
admin.site.register(DistrictUser)
admin.site.register(Session)
admin.site.register(Temporary)

