from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .forms import SearchForm
from .tables import PackageInfoTable
from .logic import PackageInfoManager, SearchManager
from django_tables2 import RequestConfig
from .tasks import trigger_package_load
from django.contrib.sites.models import Site
from django.urls import reverse
from django.conf import settings

import json

def index(request):
  return render(request, 'index.html', {'form': SearchForm()})

def result(request):
  if "query" in request.GET:
    page = request.GET.get('page', 1)
    manager = SearchManager(request.GET['query'], page=page)
    qs = manager.search()
    table = PackageInfoTable(qs)
    RequestConfig(request, paginate={"per_page": settings.SEARCH_PAGINATION_SIZE}).configure(table)
    return render(request, 'result.html', {"result_table": table})
  else:
    return HttpResponse("You need to include query! Go to /search and send the request from there.")

def get_max(request):
  page = request.GET.get('page', 1)
  manager = SearchManager(page=page)
  qs = manager.get_all()
  table = PackageInfoTable(qs)
  RequestConfig(request, paginate={"per_page": settings.SEARCH_PAGINATION_SIZE}).configure(table)
  return render(request, 'result.html', {"result_table": table})

def load_packages(request):
  manager = PackageInfoManager()
  manager.get_packages_info_from_feed()
  manager.save_package_info()
  return HttpResponse("Done!")

def schedule_package_load(request):
  trigger_package_load(request.scheme + '://' + request.get_host() + reverse('load_packages'))
  return HttpResponse('Package load scheduled!')

def search_package_info(request):
  if "query" in request.GET:
    manager = SearchManager(request.GET['query'])
    qs = manager.search()
    return JsonResponse({"result":list(qs.values())})
  else:
    return JsonResponse({"error": "You need to include query param."})
