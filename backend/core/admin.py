from django.contrib import admin

from core.models import User, OrganizationGis, Review

admin.site.register(User)
admin.site.register(OrganizationGis)
admin.site.register(Review)
