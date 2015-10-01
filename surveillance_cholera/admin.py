from django.contrib import admin
from surveillance_cholera.models import  *
from importcsvadmin.admin import ImportCSVModelAdmin
from django import forms

class ProvinceAdminImporter(forms.ModelForm):
    class Meta:
        model = Province
        fields = ('name', 'code')
        ordering = ['name']

class ProvinceAdmin(ImportCSVModelAdmin):
    importer_class = ProvinceAdminImporter

class DistrictAdminImporter(forms.ModelForm):
    class Meta:
        model = District
        fields = ('province', 'name', 'code' )
        ordering = ['name']

class DistrictAdmin(ImportCSVModelAdmin):
    importer_class = DistrictAdminImporter

class CDSAdminImporter(forms.ModelForm):
    class Meta:
        model = CDS
        fields = ('district','name', 'code')
        ordering = ['name']

class CDSAdmin(ImportCSVModelAdmin):
    importer_class = CDSAdminImporter

admin.site.register(Person)
admin.site.register(Patient)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(CDS, CDSAdmin)
admin.site.register(Reporter)
admin.site.register(Report)
admin.site.register(TrackPatientMessage)
admin.site.register(Temporary)

