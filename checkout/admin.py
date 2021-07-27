from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date', 'total', 'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'address_line_1',
              'address_line_2', 'town_or_city',  'county',
              'postcode', 'country', 'total', 'stripe_pid')

    list_display = ('order_number', 'date', 'full_name', 'total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
