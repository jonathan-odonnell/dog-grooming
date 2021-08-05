from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.utils.timezone import make_aware
from bag.context import bag_contents
from .forms import OrderForm
from .models import Order, OrderLineItem, Appointment, Coupon
from services.models import Service
from profiles.models import UserProfile
from datetime import date, datetime, timedelta
import stripe
import json


class CacheCheckoutView(View):
    http_method_names = ['post']

    def post(self, request):
        try:
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'coupon': request.session.get('coupon', ''),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)
        except Exception as e:
            messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
            return HttpResponse(content=e, status=400)


class CheckoutView(LoginRequiredMixin, View):
    form_class = OrderForm
    template_name = 'checkout/checkout.html'
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    def create_intent(self, request):
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = self.stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        return intent

    def get_context_data(self, form):
        context = {
            'form': form,
            'stripe_public_key': self.stripe_public_key,
            'client_secret': self.intent.client_secret
        }
        return context

    def get(self, request):
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('services'))

        self.intent = self.create_intent(request)

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

        context = self.get_context_data(form)
        return render(request, self.template_name, context)

    def post(self, request):
        bag = request.session.get('bag', {})
        coupon = request.session.get('coupon', {})
        coupon_qs = None
        self.intent = self.create_intent(request)
        profile = UserProfile.objects.get(user=request.user)

        if coupon:
            current_date = date.today()
            coupon_qs = get_object_or_404(
                Coupon,
                name=coupon,
                start_date_gte=current_date,
                end_date_lte=current_date
            )

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

        form = OrderForm(form_data)
        if form.is_valid():
            order = form.save(commit=False)
            order.coupon = coupon_qs
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.user_profile = profile
            order.save()

            for item_id, item_data in bag['services'].items():
                try:
                    service = Service.objects.get(id=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        service=service,
                        quantity=item_data['quantity'],
                        size=service.size,
                    )
                    for appointment in item_data['appointments']:
                        start_time = make_aware(datetime.strptime(
                            appointment, '%d/%m/%Y %H:%M'))
                        end_time = start_time + timedelta(hours=2)
                        Appointment.objects.create(
                            order=order,
                            start=start_time,
                            end=end_time
                        )
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
            context = self.get_context_data(form)
            return render(request, self.template_name, context)


class AddCouponView(View):
    def post(self, request):
        try:
            current_date = date.today()
            coupon = Coupon.objects.get(
                name=request.POST['coupon'],
                start_date__gte=current_date,
                end_date__lte=current_date
            )
            request.session['coupon'] = coupon.name
            return HttpResponse(status=200)
        except Coupon.DoesNotExist:
            return HttpResponse(status=500)


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
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
