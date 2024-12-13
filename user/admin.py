from django.contrib import admin

from .models import Client, ExternalUser, User, UserRole


class ClientAdmin(admin.ModelAdmin):
    list_display = ("__str__", "municipality", "subdomain", "status")
    search_fields = ("municipality", "subdomain", "status")


# Register your models here.

admin.site.register([User, UserRole, ExternalUser])
admin.site.register(Client, ClientAdmin)
