import django_tables2 as tables
from surveillance_cholera.models import CDS

class CDSTable(tables.Table):
    class Meta:
        model = CDS
        attrs = {"class": "table table-bordered table-condensed"}