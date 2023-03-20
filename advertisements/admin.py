from django.contrib import admin

from advertisements.models import Advertisement, Comment

# ----------------------------------------------------------------------------------------------------------------------
# Register models
admin.site.register(Advertisement)
admin.site.register(Comment)
