from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):

    readonly_fields = ('date',)

    fields = ('full_name', 'email', 'user_profile',
              'date', 'subject', 'message',)

    list_display = ('full_name', 'email', 'subject', 'date',)


admin.site.register(Contact, ContactAdmin)
