from django.shortcuts import get_object_or_404
from services.models import Service
from decimal import Decimal


def bag_contents(request):
    services = []
    grand_total = 0
    item_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_quantity in bag.items():
        service = get_object_or_404(Service, id=item_id)
        grand_total += item_quantity * service.price
        item_count += item_quantity
        services.append({
            'item_id': item_id,
            'quantity': item_quantity,
            'service': service,
        })

    tax = Decimal(grand_total * 0.2)
    total = Decimal(grand_total - tax)

    context = {
        'services': services,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'item_count': item_count,
    }

    return context
