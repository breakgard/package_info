from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import SearchForm
from .tables import PackageInfoTable
from .logic import PackageInfoManager, SearchManager
from django_tables2 import RequestConfig

def index(request):
  return render(request, 'index.html', {'form': SearchForm()})

def result(request):
  if "query" in request.GET:
    manager = SearchManager(request.GET['query'], request.GET.get('sort', None), request.GET.get('page', 1))
    qs = manager.search()
    table = PackageInfoTable(qs)
    RequestConfig(request).configure(table)
    return render(request, 'result.html', {"result_table": table})
  else:
    return HttpResponse("You need to include query! Go to /search and send the request from there.")
  return HttpResponse(f"Result will be here.")

def load_packages(request):
  manager = PackageInfoManager()
  manager.get_packages_info_from_feed()
  manager.save_package_info()
  return HttpResponse("Done!")
