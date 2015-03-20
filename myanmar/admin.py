from django.contrib.gis import admin
from myanmar import models


admin.site.register(models.Country, admin.GeoModelAdmin)
admin.site.register(models.State, admin.GeoModelAdmin)
admin.site.register(models.Township, admin.GeoModelAdmin)
