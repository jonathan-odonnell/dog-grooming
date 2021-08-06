from django.shortcuts import (
    redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
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


class CheckoutView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'checkout/checkout.html'
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    google_api_key = settings.GOOGLE_API_KEY

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

    def get_initial(self):
        profile = UserProfile.objects.get(user=self.request.user)
        initial = {
            'full_name': profile.user.get_full_name(),
            'email': profile.user.email,
            'phone_number': profile.phone_number,
            'address_line_1': profile.address_line_1,
            'address_line_2': profile.address_line_2,
            'town_or_city': profile.town_or_city,
            'county': profile.county,
            'country': profile.country,
            'postcode': profile.postcode,
        }
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_public_key'] = self.stripe_public_key
        context['client_secret'] = self.intent.client_secret
        context['google_api_key'] = self.google_api_key
        return context

    def get_success_url(self):
        return reverse(
            'checkout_success', args=[self.object.order_number])

    def get(self, request):
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request, "There's nothing in your bag at the moment")
            return redirect(reverse('services'))

        self.object = None
        self.intent = self.create_intent(request)
        self.initial = self.get_initial()
        return self.render_to_response(self.get_context_data())

    def post(self, request):
        bag = request.session.get('bag', {})
        coupon = request.session.get('coupon', {})
        coupon_qs = None
        self.intent = self.create_intent(request)
        profile = UserProfile.objects.get(user=request.user)

        if coupon:
            current_date = make_aware(date.today())
            coupon_qs = get_object_or_404(
                Coupon,
                name=coupon,
                start_date_gte=current_date,
                end_date_lte=current_date
            )

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, profile, coupon_qs, bag)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, profile, coupon, bag):
        self.object = form.save(commit=False)
        self.object.coupon = coupon
        pid = self.request.POST.get('client_secret').split('_secret')[0]
        self.object.stripe_pid = pid
        self.object.user_profile = profile
        self.object.save()

        for item_id, item_data in bag['services'].items():
            try:
                service = Service.objects.get(id=item_id)
                OrderLineItem.objects.create(
                    order=self.object,
                    service=service,
                    quantity=item_data['quantity'],
                    size=service.size,
                )
                for appointment in item_data['appointments']:
                    start_time = make_aware(datetime.strptime(
                        appointment, '%d/%m/%Y %H:%M'))
                    end_time = start_time + timedelta(hours=2)
                    appointment_exists = Appointment.objects.get(
                        start=start_time, end=end_time).exists()
                    if not appointment_exists:
                        Appointment.objects.create(
                            order=self.object,
                            start=start_time,
                            end=end_time
                        )
                    else:
                        messages.error(self.request,  "Unable to book the appointment you selected. \
                            Please try again")
                        return redirect(reverse('service_appointments',
                                                args=[int(item_id)]))

            except Service.DoesNotExist:
                messages.error(self.request, "One of the services in your bag wasn't found in \
                        our database. Please call us for assistance!")
                self.object.delete()
                return redirect(reverse('bag'))

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your form. \
                Please double check your information.')
        return self.render_to_response(self.get_context_data(form=form))


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


class CheckoutSuccessView(LoginRequiredMixin, DetailView):
    """ Handle successful checkouts """
    context_object_name = 'order'
    template_name = "checkout/checkout_success.html"

    def get_object(self):
        return get_object_or_404(
            Order, order_number=self.kwargs['order_number'])

    def get(self, request, order_number, *args, **kwargs):
        self.object = self.get_object()
        if 'bag' in request.session:
            del request.session['bag']
        return self.render_to_response(self.get_context_data())
