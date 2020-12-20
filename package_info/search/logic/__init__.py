import requests
import feedparser
import re
import logging
from elasticsearch_dsl import Q
from django.conf import settings

from search.models import PackageInfo, INDEXED_FIELDS
from search.documents import PackageInfoDocument
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class PackageInfoManager():

  def __init__(self):
    logger.debug("Setting up PackageInfoManager")
    self.feed_url = settings.SEARCH_PACKAGE_FEED_URL
    self.package_info_repo_url = settings.SEARCH_PACKAGE_INFO_REPO_URL
    self.connection_timeout = settings.SEARCH_PACKAGE_INFO_FETCH_TIMEOUT
    self.name_regex = re.compile('^.*/([^/]+)/$')
    self.packages_info = []
    logger.debug("Setting up PackageInfoManger done")

  def __get_name_from_package_id(self, package_id):
    return self.name_regex.match(package_id).groups()[0]

  def get_packages_info_from_feed(self):
    logger.debug("PackageInfoManager get_packages_info_from_feed invoked")
    packages_info = []
    packages_feed = feedparser.parse(self.feed_url)
    logger.info("PackageInfoManager feed parsed")
    for package in packages_feed.entries:
      package_name = self.__get_name_from_package_id(package['id'])
      r = requests.get(f"{self.package_info_repo_url}/{package_name}/json", timeout=self.connection_timeout)
      if r.status_code == 200:
        package_info = r.json()
        logger.info(f"PackageInfoManager Found package {package['id']}")
        packages_info.append({'_id':package['id'], 'repo_info': package_info})
      else:
        logger.error(f"Error getting package info: {r.status_code}")
        logger.error(r.text)
    self.packages_info = packages_info

  def save_package_info(self):
    logger.debug("PackageInfoManager save_package_info invoked")
    for package_info in self.packages_info:
      repo_info = package_info['repo_info']['info']
      obj = None
      try:
        obj = PackageInfo.objects.get(package_id=package_info['_id'])
        logger.info(f"PackageInfoManager Modifying existing package info {package_info['_id']}")
        obj.package_id = str(package_info['_id'])
      except ObjectDoesNotExist:
        logger.info(f"PackageInfoManager Creating package info for {package_info['_id']}")
        obj = PackageInfo(package_id=str(package_info['_id']))
      obj.description_content_type = str(repo_info['description_content_type'])
      for field in INDEXED_FIELDS:
        setattr(obj, field, str(repo_info[field]))
      obj.save()


class SearchManager():

  def __init__(self, query=None, page=1):
    logger.debug("Setting up SearchManager")
    self.query = query
    self.page = page
    logger.debug("Setting up SearchManager done")

  def __get_queryset(self, q):
    search_query = PackageInfoDocument.search().params(size=settings.SEARCH_MAX_DOCUMENTS_RETURNED).query(q)
    queryset = search_query.to_queryset()
    return queryset

  def get_max(self):
    logger.debug("SearchManager get_max invoked")
    q = Q("match_all")
    return self.__get_queryset(q)

  def search(self):
    logger.debug("SearchManager search invoked")
    q = Q("multi_match", query=self.query, fields=INDEXED_FIELDS)
    return self.__get_queryset(q)
