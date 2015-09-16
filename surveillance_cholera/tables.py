import django_tables2 as tables
from surveillance_cholera.models import CDS, Patient, Report
from django_tables2.utils import A  # alias for Accessor

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

class PatientsTable(tables.Table):
    name = tables.Column(verbose_name="Name of CDS ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_patients_by_code', args=[A('detail')], orderable=False, empty_values=(), verbose_name='Click for details')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}

class Patients2Table(tables.Table):
    name = tables.Column(verbose_name="Name of District ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_patients_by_code', args=[A('detail')], orderable=False, empty_values=(), verbose_name='Click for details')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}

class Patients3Table(tables.Table):
    name = tables.Column(verbose_name="Name of Province ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_patients_by_code', args=[A('detail')], orderable=False, empty_values=(), verbose_name='Click for details')

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}

class ReportTable(tables.Table):
    class Meta:
        model = Report
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" ,  "data-show-export":"true"}