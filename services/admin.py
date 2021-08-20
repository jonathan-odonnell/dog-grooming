from django.contrib import admin
from .models import Service, Price, Availability, Appointment
from django_dramatiq.models import Task


class PriceAdminInline(admin.StackedInline):
    model = Price
    extra = 1


class ServiceAdmin(admin.ModelAdmin):
    inlines = (PriceAdminInline,)
    ordering = ('id',)


class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ('task_id', 'last_updated',)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Availability)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.unregister(Task)
