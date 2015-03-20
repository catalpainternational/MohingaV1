from django.contrib import admin

from profiles import models


admin.site.register(models.OrganisationProfile)
admin.site.register(models.Contact)
admin.site.register(models.Person)
