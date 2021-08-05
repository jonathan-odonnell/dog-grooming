from django.urls.base import reverse
from django.views.generic.base import View, TemplateView
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from services.models import Service


class BagView(TemplateView):
    template_name = "bag/bag.html"


class AddServiceToBagView(View):
    """ Add the specified service to the shopping bag """
    def post(self, request, item_id):
        service = get_object_or_404(Service, id=item_id)
        bag = request.session.get('bag', {'services': {}})

        if item_id in list(bag['services'].keys()):
            bag['services'][item_id]['quantity'] += 1
            bag['services'][item_id]['appointments'].append(
                request.POST['appointment'])
            messages.success(
                request, f'Added {service.name} to bag')
        else:
            bag['services'][item_id] = {
                'quantity': 1,
                'appointments': [request.POST['appointment']]
            }
            messages.success(request, f'Added {service.name} to bag')

        request.session['bag'] = bag
        return redirect(reverse('services'))


class RemoveServiceFromBagView(View):
    """ Removes the specified service from the shopping bag """
    def post(self, request, item_id):
        try:
            service = get_object_or_404(Service, id=item_id)
            bag = request.session.get('bag', {})
            bag['services'].pop(item_id)
            messages.success(request, f'Removed {service.name} from your bag')
            request.session['bag'] = bag
            return HttpResponse(status=200)

        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)
