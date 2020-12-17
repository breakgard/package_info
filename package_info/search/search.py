from .documents import PackageInfoDocument
from elasticsearch_dsl import Q

class SearchManager():

  def __init__(self, query):
    self.query = query

  def search(self):
    hits = []
    #, fields=['author', 'author_email', 'description', 'keywords', 'version', 'maintainer', 'maintainer_email', 'name']
    q = Q("multi_match", query=self.query, fields=['author', 'author_email', 'description', 'keywords', 'version', 'maintainer', 'maintainer_email', 'name'])
    search = PackageInfoDocument.search().query(q).execute()
    print("executed")
    print(dir(search.hits))
    print(search.hits.total)
    for hit in search.hits.hits:
      print(hit)
      hits.append(hit['_source'])
    return hits
