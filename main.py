#!/usr/bin/env python3

from backend import package_info
import pprint
import pdb
import logging

def main():
  logger = logging.getLogger()
  logger.setLevel('DEBUG')
  manager = package_info.PackageInfoManager()
  manager.get_packages_info_from_feed()
  manager.upload_packages_to_db()
  manager.upload_packages_to_full_text_search()

if __name__ == '__main__':
  main()
