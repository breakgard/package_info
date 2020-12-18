from background_task import background
from django.conf import settings
from django.urls import path
import pdb
import requests

@background(schedule=settings.SEARCH_PACKAGE_LOAD_INTERVAL_MINUTES * 60)
def trigger_package_load(package_load_url):
  r = requests.get(package_load_url, timeout=settings.SEARCH_PACKAGE_LOAD_TIMEOUT)
  if r.ok:
    print("Package load done.")
  else:
    print("Packaged failed!")
