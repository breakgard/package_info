from django.db import models

INDEXED_FIELDS = ['author', 'author_email', 'description', 'keywords', 'version', 'maintainer', 'maintainer_email', 'name']

# Create your models here.
class PackageInfo(models.Model):
    package_id = models.CharField(db_index=True, max_length=255, default='')
    name = models.CharField(max_length=255, default='')
    author = models.CharField(max_length=255, default='')
    author_email = models.CharField(max_length=255, default='')
    description = models.TextField(default='')
    description_content_type = models.CharField(max_length=255, default='')
    keywords = models.CharField(max_length=255, default='')
    version = models.CharField(max_length=255, default='')
    maintainer = models.CharField(max_length=255, default='')
    maintainer_email = models.CharField(max_length=255, default='')
    
