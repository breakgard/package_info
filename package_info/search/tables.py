import django_tables2 as tables
from .models import PackageInfo
from django.utils.safestring import mark_safe
from markdownify.templatetags.markdownify import markdownify

def handle_emails(emails_string):
  emails = "<div>"
  for email in emails_string.split(','):
    emails = f"{emails}<a href='mailto:{email}'>{email}</a><br />"
  emails = f"{emails}</div>"
  return mark_safe(emails)

class PackageInfoTable(tables.Table):
    class Meta:
        model = PackageInfo
        orderable = True
        exclude = ('description_content_type','id',)
    def render_package_id(self, value):
      return mark_safe(f'<a href="{value}">{value}</a>')

    def render_author_email(self, value):
      return handle_emails(value)

    def render_maintainer_email(self, value):
      return handle_emails(value)

    def render_description(self, value, record):
      if record.description_content_type == 'text/markdown':
        return mark_safe(f'<div style="overflow-y: auto; height: 300px;" >{markdownify(value)}</div>')
      else:
        return value
