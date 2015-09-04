import django_tables2 as tables
from surveillance_cholera.models import CDS, Patient
from django_tables2.utils import A  # alias for Accessor

class CDSTable(tables.Table):
    class Meta:
        model = CDS
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-show-toggle":"true", "data-show-export":"true"}

class PatientTable(tables.Table):
    class Meta:
        model = Patient
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-show-toggle":"true", "data-show-export":"true"}

class PatientsTable(tables.Table):
    name = tables.Column(verbose_name="Name of CDS ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_by_code', args=[A('detail')], orderable=False, empty_values=())

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}

class Patients2Table(tables.Table):
    name = tables.Column(verbose_name="Name of District ")
    total = tables.Column()
    nc = tables.Column()
    hospi = tables.Column()
    sorties = tables.Column()
    deces = tables.Column()
    detail = tables.LinkColumn('get_by_code', args=[A('detail')], orderable=False, empty_values=())

    class Meta:
        attrs = {"class": "table ", "data-toggle":"table", "data-search":"true" ,"data-show-columns":"true" , "data-click-to-select":"true", "data-show-export":"true"}