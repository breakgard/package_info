from django.db import models

# Create your models here.
class PackageInfo(models.Model):
    package_id = models.CharField(db_index=True)
    name = models.CharField()
    author = models.CharField()
    author_email = models.CharField()
    description = models.TextField()
    keywords = models.CharField()
    version = models.CharField()
    maintainer = models.CharField()
    maintainer_email = models.CharField()
