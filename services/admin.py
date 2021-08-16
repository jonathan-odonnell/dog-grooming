from django.contrib import admin
from .models import Service, Price, Availability, Appointment


class PriceAdminInline(admin.StackedInline):
    model = Price
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    inlines = (PriceAdminInline,)


class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'last_updated',)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Availability)
admin.site.register(Appointment, AppointmentAdmin)
