from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Company

admin.site.register(Company, UserAdmin)
