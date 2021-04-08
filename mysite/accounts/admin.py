from django.contrib import admin
from django.contrib.auth.models import Group


admin.site.unregister(Group)
site_title = "Sawaal Admin"
# change admin interface
admin.site.index_title = site_title
admin.site.site_header = site_title
admin.site.site_title = site_title
admin.site.site_url = "/"
