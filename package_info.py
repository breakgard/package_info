import requests
import feedparser
import re
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from configparser import ConfigParser
from pymongo import MongoClient, ReplaceOne

class PackageInfoManager():

  def __init__(self, config_file='config.conf'):
    config = ConfigParser()
    config.read(config_file)
    self.feed_url = config['DEFAULT']['feed_url']
    self.package_info_repo_url = config['DEFAULT']['package_info_repo_url']
    self.connection_timeout = config['DEFAULT']['connection_timeout']
    self.true_id_regex = re.compile('^.*/([^/]+)/$')
    self.packages_info = []
    self.db_config = config['db']
    self.full_text_config = config['full_text_search']

  def __get_true_id_from_package_id(self, package_id):
    return self.true_id_regex.match(package_id).groups()[0]

  def __get_db_conn(self):
    mongodb_uri = 'mongodb://%s:%s@%s'
    if bool(self.db_config['auth']):
      mongodb_uri = f"{mongodb_uri}{self.db_config['user_name']}:{self.db_config['user_pass']}@{self.db_config['host']}:{self.db_config['port']}"
    else:
      mongodb_uri = f"{mongodb_uri}{self.db_config['host']}:{self.db_config['port']}"
    return MongoClient(mongodb_uri)

  def __get_full_text_conn(self):
    return Elasticsearch([{'host':self.full_text_config['host'],'port':self.full_text_config['port']}])

  def __get_indexed_fields_from_packages_info(self):
    for package in self.packages_info:
      repo_info = package['repo_info']
      indexed_document = {'_id': package['_id'],
                          '_index': self.full_text_config['index_name'],
                          'author': repo_info['author'],
                          'author_email':repo_info['author_email'],
                          'description', repo_info['description'],
                          'keywords':repo_info['keywords'],
                          'version':repo_info['version'],
                          'maintainer': repo_info['maintainer'],
                          'maintainer_email': repo_info['maintainer_email'],
                          'name': repo_info['name'] }
      yield indexed_fields

  def get_packages_info_from_feed(self):
    packages_info = []
    packages_feed = feedparser.parse(self.feed_url)
    for package in packages_feed.entries:
      package_id = self.__get_true_id_from_package_id(package['id'])
      package_info = requests.get(f"{self.package_info_repo_url}/{package_id}/json", timeout=self.connection_timeout).json()
      packages_info.append({'_id':package['id'], 'repo_info': package_info})
    self.packages_info = packages_info

  def get_packages_info_from_db(self):
    with self.__get_db_conn() as db_conn:
      self.packages_info = list(db_conn[self.db_config['db_name']][self.db_config['col_name']].find({}))

  def upload_packages_to_db(self):
    requests = []
    for package_info in packages_info:
      requests.append(ReplaceOne({'_id':package_info['_id']}, package_info, upsert=True))
    with self.__get_db_conn() as db_conn:
      db_conn[self.db_config['db_name']][self.db_config['col_name']].bulk_write(requests)

  def upload_packages_to_full_text_search(self):
    full_text_conn = self.__get_full_text_conn()
    bulk(full_text_conn, self.__get_indexed_fields_from_packages_info())
