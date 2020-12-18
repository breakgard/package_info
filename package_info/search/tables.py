import django_tables2 as tables
from .models import PackageInfo

class PackageInfoTable(tables.Table):
    class Meta:
        model = PackageInfo
        orderable = True
