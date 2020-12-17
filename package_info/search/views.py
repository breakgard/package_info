from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import SearchForm
from .load_package_info import PackageInfoManager
from .search import SearchManager

def index(request):
  return render(request, 'index.html', {'form': SearchForm()})

def result(request):
  if "query" in request.POST:
    manager = SearchManager(request.POST['query'])
    hits = manager.search()
    return render(request, 'result.html', {'hits': hits})
  else:
    return HttpResponse("You need to include query! Go to /search and send the request from there.")
  return HttpResponse(f"Result will be here.")

def load_packages(request):
  manager = PackageInfoManager()
  manager.get_packages_info_from_feed()
  manager.save_package_info()
  return HttpResponse("Done!")
