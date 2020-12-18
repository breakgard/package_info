from django.db import models

INDEXED_FIELDS = ['author', 'author_email', 'description', 'keywords', 'version', 'maintainer', 'maintainer_email', 'name']

# Create your models here.
class PackageInfo(models.Model):
    package_id = models.CharField(db_index=True, max_length=255)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    author_email = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    version = models.CharField(max_length=255)
    maintainer = models.CharField(max_length=255)
    maintainer_email = models.CharField(max_length=255)
