import requests
import feedparser
import re
import logging
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from configparser import ConfigParser
from pymongo import MongoClient, ReplaceOne
from urllib.parse import quote_plus

class PackageInfoManager():

  def __init__(self, config_file='config.conf'):
    logging.debug("Setting up PackageInfoManager")
    config = ConfigParser()
    config.read(config_file)
    self.feed_url = config['DEFAULT']['feed_url']
    self.package_info_repo_url = config['DEFAULT']['package_info_repo_url']
    self.connection_timeout = int(config['DEFAULT']['connection_timeout'])
    self.name_regex = re.compile('^.*/([^/]+)/$')
    self.packages_info = []
    self.db_config = config['db']
    self.full_text_config = config['full_text_search']
    logging.debug("Setting up PackageInfoManger done")

  def __get_name_from_package_id(self, package_id):
    return self.name_regex.match(package_id).groups()[0]

  def __get_db_conn(self):
    mongodb_uri = 'mongodb://'
    if bool(self.db_config['auth']):
      mongodb_uri = f"{mongodb_uri}{quote_plus(self.db_config['user_name'])}:{quote_plus(self.db_config['user_pass'])}@{self.db_config['host']}:{self.db_config['port']}"
    else:
      mongodb_uri = f"{mongodb_uri}{self.db_config['host']}:{self.db_config['port']}"
    return MongoClient(mongodb_uri)

  def __get_full_text_conn(self):
    return Elasticsearch([{'host':self.full_text_config['host'],'port':self.full_text_config['port']}])

  def __get_indexed_fields_from_packages_info(self):
    for package in self.packages_info:
      repo_info = package['repo_info']['info']
      indexed_document = {'_id': package['_id'],
                          '_index': self.full_text_config['index_name'],
                          '_doc': {'author': repo_info['author'],
                          'author_email': repo_info['author_email'],
                          'description': repo_info['description'],
                          'keywords': repo_info['keywords'],
                          'version': repo_info['version'],
                          'maintainer': repo_info['maintainer'],
                          'maintainer_email': repo_info['maintainer_email'],
                          'name': repo_info['name']}
                          }
      yield indexed_document

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

  def get_packages_info_from_db(self):
    with self.__get_db_conn() as db_conn:
      self.packages_info = list(db_conn[self.db_config['db_name']][self.db_config['col_name']].find({}))

  def upload_packages_to_db(self):
    requests = []
    for package_info in self.packages_info:
      requests.append(ReplaceOne({'_id':package_info['_id']}, package_info, upsert=True))
    with self.__get_db_conn() as db_conn:
      db_conn[self.db_config['db_name']][self.db_config['col_name']].bulk_write(requests)

  def upload_packages_to_full_text_search(self):
    full_text_conn = self.__get_full_text_conn()
    bulk(full_text_conn, self.__get_indexed_fields_from_packages_info())
