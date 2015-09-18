import django_tables2 as tables
from surveillance_cholera.models import CDS, Patient, Report
from django_tables2.utils import A  # alias for Accessor
from django.utils.safestring import SafeString

class CDSTable(tables.Table):
    class Meta:
        model = CDS
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true"}

class PatientTable(tables.Table):
    province = tables.Column(accessor='cds.district.province')
    district = tables.Column(accessor='cds.district')

    class Meta:
        model = Patient
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true"}
        exclude = ('id', 'colline_name')
        sequence = ("patient_id", "...", "cds")

    def render_intervention(self, value):
        if value.upper() in ['DD']:
            return 'Deces'
        if value.upper() in ['HOSPI']:
            return 'Hospitalisation'
        if value.upper() in ['PR']:
            return 'Reference'
        if value.upper() in ['DESH']:
            return 'Non Hospitalise'
        else :
            return value

    def render_age(self, value):
        if value.upper() in ['A1']:
            return 'Inf 5 ans'
        if value.upper() in ['A2']:
            return 'Sup 5 ans'
        else:
            return value

    def render_exit_status(self, value):
        if value.upper() in ['PR']:
            return 'Reference'
        if value.upper() in ['PD']:
            return 'Deces'
        if value.upper() in ['PG']:
            return 'Gueri'
        else:
            return value

    def render_patient_id(self, value, record):
        return SafeString('''<a href="/cholera/patient/%s">%s</a>''' % (record.id, value))


class PatientsTable(tables.Table):
    cds_id = tables.Column()
    name = tables.Column(verbose_name="Name of CDS ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_patients_by_code', args=[A('detail')], orderable=False, empty_values=(), verbose_name='Click for details')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}
        exclude = ('cds_id',)

    # def render_detail(self, value, record):
    #     return SafeString('''<a href="/cholera/cds/%s">%s</a>''' % (record['cds_id'], value))

class Patients2Table(tables.Table):
    district_id = tables.Column()
    name = tables.Column(verbose_name="Name of District ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.Column()

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}
        exclude = ('district_id',)

    def render_detail(self, value, record):
        return SafeString('''<a href="/cholera/district/%s">%s</a>''' % (record['district_id'], value))

class Patients3Table(tables.Table):
    name = tables.Column(verbose_name="Name of Province ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('province_detail', args=[A('detail')], orderable=False, empty_values=(), verbose_name='Click for details')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}

class ReportTable(tables.Table):
    class Meta:
        model = Report
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true"}