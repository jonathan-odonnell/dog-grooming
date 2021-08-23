from django.contrib import admin
from .models import Service, Price, Availability, Appointment
from django_dramatiq.models import Task


class PriceAdminInline(admin.StackedInline):
    model = Price
    extra = 4
    max_num = 4
    can_delete = False


class ServiceAdmin(admin.ModelAdmin):
    inlines = (PriceAdminInline,)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'reserved', 'confirmed')
    list_filter = ('reserved', 'confirmed',)
    readonly_fields = ('task_id', 'last_updated',)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Availability)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.unregister(Task)
