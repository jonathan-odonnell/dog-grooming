from django.shortcuts import get_object_or_404
from services.models import Service


def bag_contents(request):
    services = []
    total = 0
    item_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        service = get_object_or_404(Service, id=item_id)
        total += item_data * service.price
        item_count += item_data
        services.append({
            'item_id': item_id,
            'quantity': item_data,
            'service': service,
        })

    context = {
        'services': services,
        'total': total,
        'item_count': item_count,
    }

    return context
