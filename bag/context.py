from checkout.models import Coupon
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
        for size, size_data in item_data.items():
            price = get_object_or_404(Price, service=service, size=size)
            order_total += item_data[size]['quantity'] * price.price
            item_count += item_data[size]['quantity']
            appointments = []
            for appointment in size_data['appointments']:
                appointment = get_object_or_404(Appointment, id=appointment)
                appointments.append(appointment)
            services.append({
                'item_id': item_id,
                'service': service,
                'item_price': price,
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
