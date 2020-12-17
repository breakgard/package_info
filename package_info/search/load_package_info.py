import requests
import feedparser
import re
import logging

from .models import PackageInfo
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
class PackageInfoManager():

  def __init__(self):
    logging.debug("Setting up PackageInfoManager")
    self.feed_url = settings.SEARCH_PACKAGE_FEED_URL
    self.package_info_repo_url = settings.SEARCH_PACKAGE_INFO_REPO_URL
    self.connection_timeout = settings.SEARCH_PACKAGE_INFO_FETCH_TIMEOUT
    self.name_regex = re.compile('^.*/([^/]+)/$')
    self.packages_info = []
    logging.debug("Setting up PackageInfoManger done")

  def __get_name_from_package_id(self, package_id):
    return self.name_regex.match(package_id).groups()[0]

  def get_packages_info_from_feed(self):
    packages_info = []
    packages_feed = feedparser.parse(self.feed_url)
    for package in packages_feed.entries:
      package_name = self.__get_name_from_package_id(package['id'])
      r = requests.get(f"{self.package_info_repo_url}/{package_name}/json", timeout=self.connection_timeout)
      if r.status_code == 200:
        package_info = r.json()
        packages_info.append({'_id':package['id'], 'repo_info': package_info})
      else:
        logging.error(f"Error getting package info: {r.status_code}")
        logging.error(r.text)
    self.packages_info = packages_info

  def save_package_info(self):
    for package_info in self.packages_info:
      repo_info = package_info['repo_info']['info']
      try:
        obj = PackageInfo.objects.get(package_id=package_info['_id'])
        for key in obj:
          obj[key] = repo_info[key]
        obj.save()
      except ObjectDoesNotExist:
        PackageInfo(
                    package_id=package['_id'],
                    author=repo_info['author'],
                    author_email=repo_info['author_email'],
                    description=repo_info['description'],
                    keywords=repo_info['keywords'],
                    version=repo_info['version'],
                    maintainer=repo_info['maintainer'],
                    maintainer_email=repo_info['maintainer_email'],
                    name=repo_info['name']
        ).save)()
