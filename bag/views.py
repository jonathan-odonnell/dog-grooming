from django.urls.base import reverse
from django.views.generic.base import View, TemplateView
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from services.models import Service, Appointment
from datetime import datetime
from django.utils.timezone import make_aware


class BagView(TemplateView):
    template_name = "bag/bag.html"


class AddServiceToBagView(View):
    """ Add the specified service to the shopping bag """

    def post(self, request, item_id):
        service = get_object_or_404(Service, id=item_id)
        bag = request.session.get('bag', {'services': {}})
        size = request.POST['size']
        start_time = make_aware(datetime.strptime(
            request.POST['appointment'], '%d/%m/%Y %H:%M'))

        try:
            appointment = Appointment.objects.get(
                start_time=start_time, reserved=False)
            appointment.reserved = True
            appointment.comments = request.POST['comments']
            appointment.save()

            if item_id in list(bag['services'].keys()):
                if size in bag['services'][item_id].keys():
                    bag['services'][item_id][size]['quantity'] += 1
                    bag['services'][item_id][size]['appointments'].append(
                        appointment.id)
                    messages.success(
                        request, f'Added {service.name} for {size} dog to bag')
                else:
                    bag['services'][item_id][size] = {
                        'quantity': 1,
                        'appointments': [appointment.id]
                    }
                    messages.success(
                        request, f'Added {service.name} for {size} dog to bag')
            else:
                bag['services'][item_id] = {
                    'quantity': 1,
                    'appointments': [appointment.id]
                }
                messages.success(
                    request, f'Added {service.name} for {size} dog to bag')

            request.session['bag'] = bag
            return redirect(reverse('services'))

        except Appointment.DoesNotExist:
            messages.success(
                request, 'Appointment is no longer available. \
                    Please try again.')
            return redirect(request.META.get('HTTP_REFERER'))


class RemoveServiceFromBagView(View):
    """ Removes the specified service from the shopping bag """

    def post(self, request, item_id):
        try:
            service = get_object_or_404(Service, id=item_id)
            bag = request.session.get('bag', {})
            size = request.POST['size']
            appointment = int(request.POST['appointment'])

            if len(list(bag['services'][item_id].keys())) == 1:
                bag['services'].pop(item_id)
            elif bag['services'][item_id][size]['quantity'] == 1:
                bag['services'][item_id].pop(size)
            else:
                bag['services'][item_id][size]['quantity'] -= 1
                bag['services'][item_id]['appointments'].remove(appointment)

            appointment = Appointment.objects.get(id=appointment)
            appointment.comments = None
            appointment.reserved = False
            appointment.save()

            messages.success(
                request, f'Removed {service.name} for {size} \
                    dog from your bag')
            request.session['bag'] = bag
            return HttpResponse(status=200)

        except Exception as e:
            messages.error(request, f'Error removing item: {e}')
            return HttpResponse(status=500)
