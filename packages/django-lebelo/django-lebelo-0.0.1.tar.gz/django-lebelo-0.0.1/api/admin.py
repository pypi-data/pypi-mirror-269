from django.contrib import admin

from .models import DeveloperAccount, Permission

admin.site.register(DeveloperAccount)
admin.site.register(Permission)
