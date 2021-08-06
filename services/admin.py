from django.contrib import admin
from .models import Service, Price, Availability


class PriceAdminInline(admin.StackedInline):
    model = Price
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    inlines = (PriceAdminInline,)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Availability)
