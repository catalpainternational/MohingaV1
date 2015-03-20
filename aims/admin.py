from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import UserOrganisation


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserOrganisationInline(admin.StackedInline):
    model = UserOrganisation
    verbose_name_plural = 'User Organisations'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserOrganisationInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
