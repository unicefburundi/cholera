from django.contrib import admin
from surveillance_cholera.models import  *
from import_export import resources
from import_export.admin import ExportMixin

class ProvinceAdminResource(resources.ModelResource):
    class Meta:
        model = Province
        fields = ('name', 'code')
        ordering = ['name']

class ProvinceAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProvinceAdminResource
    list_display = ('name', 'code', )
    search_fields = ('name', 'code', )

class DistrictAdminResource(resources.ModelResource):
    class Meta:
        model = District
        fields = ('province__name', 'name', 'code' )
        ordering = ['name']

class DistrictAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = DistrictAdminResource
    list_display = ('name', 'code', 'province')
    search_fields = ('name', 'code', 'province__name')

    def province(self, obj):
        return obj.province.name

class CDSAdminResource(resources.ModelResource):
    class Meta:
        model = CDS
        fields = ('district__name','name', 'code', 'district__province__name')
        ordering = ['name']

class CDSAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CDSAdminResource
    list_display = ('name', 'code', 'status', 'district', 'province')
    search_fields = ('name', 'code', 'district__name', 'district__province__name')

    def district(self, obj):
        return obj.district.name

    def province(self, obj):
        return obj.district.province.name

class PatientAdminResource(resources.ModelResource):
    class Meta:
        model = Patient
        fields = ('patient_id', 'colline_name', 'age', 'intervention', 'date_entry', 'exit_status', 'cds__name', 'cds__district__name', 'cds__district__province__name')
        ordering = ['name']

class PatientAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PatientAdminResource
    date_hierarchy = 'date_entry'
    list_display = ('patient_id', 'colline_name', 'age', 'intervention', 'date_entry', 'exit_status', 'cds', 'district', 'province')
    list_filter = ('age', 'intervention', 'exit_status')
    search_fields = ('cds__name', 'patient_id', 'colline_name', 'cds__district__name', 'cds__district__province__name')

    def district(self, obj):
        return obj.cds.district.name

    def province(self, obj):
        return obj.cds.district.province.name

admin.site.register(Person)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(CDS, CDSAdmin)
admin.site.register(Reporter)
admin.site.register(Report)
admin.site.register(TrackPatientMessage)
admin.site.register(Temporary)
admin.site.register(UserProfile)

