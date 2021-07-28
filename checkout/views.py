from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
from bag.context import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from services.models import Service
from profiles.models import UserProfile
import stripe
import json


class CacheCheckoutView(View):
    http_method_names = ['POST']

    def post(request):
        try:
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
            return HttpResponse(content=e, status=400)


class CheckoutView(View):
    form_class = OrderForm
    template_name = 'checkout/checkout.html'
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    def get(self, request):
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('services'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = self.stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                form = self.form_class(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'address_line_1': profile.address_line_1,
                    'address_line_2': profile.address_line_2,
                    'town_or_city': profile.town_or_city,
                    'county': profile.county,
                    'country': profile.country,
                    'postcode': profile.postcode,
                })
            except UserProfile.DoesNotExist:
                form = self.form_class()
        else:
            form = self.form_class()

        context = {
            'form': form,
            'stripe_public_key': self.stripe_public_key,
            'client_secret': intent.client_secret
        }

        return render(request, self.template_name, context)

    def post(self, request):
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address_line_1': request.POST['address_line_1'],
            'address_line_2': request.POST['address_line_2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.save()

            for item_id, item_quantity in bag.items():
                try:
                    service = Service.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        service=service,
                        quantity=item_quantity,
                        size=service.size,
                    )
                    order_line_item.save()
                except Service.DoesNotExist:
                    messages.error(request, (
                        "One of the services in your bag wasn't found in \
                            our database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('bag'))
            return redirect(reverse(
                'checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')


class CheckoutSuccessView(TemplateView):
    """ Handle successful checkouts """

    template_name = "checkout/checkout_success.html"

    def get(self, request, order_number, *args, **kwargs):
        self.order = get_object_or_404(Order, order_number=order_number)
        if 'bag' in request.session:
            del request.session['bag']
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        return context
