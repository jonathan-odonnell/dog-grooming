from orders.models import Coupon
from django.shortcuts import get_object_or_404
from services.models import Appointment, Service, Price
from decimal import Decimal
from datetime import date


def bag_contents(request):
    services = []
    order_total = 0
    grand_total = 0
    discount = 0
    item_count = 0
    bag = request.session.get('bag', {'services': {}})
    coupon = request.session.get('coupon', '')

    for item_id, item_data in bag['services'].items():
        service = get_object_or_404(Service, id=item_id)
        if isinstance(item_data, int):
            item_price = get_object_or_404(Price, service=service, size=None)
            order_total += item_data * item_price.price
            item_count += item_data
            services.append({
                'item_id': item_id,
                'service': service,
                'item_price': item_price,
                'quantity': item_data,
            })
        else:
            for size, size_data in item_data.items():
                item_price = get_object_or_404(
                    Price, service=service, size=size)
                order_total += item_data[size]['quantity'] * item_price.price
                item_count += item_data[size]['quantity']
                appointments = []
                for appointment in size_data['appointments']:
                    for appointment_id, taxi in appointment.items():
                        appointment = get_object_or_404(
                            Appointment, id=appointment_id)
                        appointments.append({
                            'appointment': appointment,
                            'taxi': taxi,
                            'price': item_price.price + Decimal(10.00)
                        })
                services.append({
                    'item_id': item_id,
                    'service': service,
                    'item_price': item_price,
                    'quantity': item_data[size]['quantity'],
                    'appointments': appointments,
                })

    if coupon:
        current_date = date.today()
        coupon_qs = get_object_or_404(
            Coupon,
            name=coupon,
            start_date_gte=current_date,
            end_date_lte=current_date
        )
        discount = coupon_qs.amount

    grand_total = Decimal(order_total - discount)

    context = {
        'bag_services': services,
        'order_total': order_total,
        'coupon': coupon,
        'discount': discount,
        'grand_total': grand_total,
        'item_count': item_count,
    }

    return context
