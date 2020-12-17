from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import SearchForm
from .load_package_info import PackageInfoManager

def index(request):
  return render(request, 'index.html', {'form': SearchForm()})

def result(request):
  for item in request.POST.items():
    print(item)
  return HttpResponse(f"Result will be here.")

def load_packages(request):
  manager = PackageInfoManager()
  manager.get_packages_info_from_feed()
  manager.save_package_info()
  return HttpResponse("Done!")
