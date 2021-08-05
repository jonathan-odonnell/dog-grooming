from dog_groming.settings import GOOGLE_API_KEY
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm


class ProfileView(LoginRequiredMixin, View):
    """ Display the user's profile. """

    form_class = UserProfileForm
    template_name = 'profiles/profile.html'
    google_api_key = settings.GOOGLE_API_KEY

    def get(self, request):
        form = self.form_class(initial={'email_address': request.user.email})
        return render(request, self.template_name, {'form': form, 'google_api_key': self.google_api_key})

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = self.form_class(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save()
            profile.user.email = request.POST['email_address']
            profile.user.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')

        return render(request, self.template_name, {'form': form, 'google_api_key': self.google_api_key})


class OrdersView(LoginRequiredMixin, TemplateView):
    """ Display the user's orders. """
    template_name = 'profiles/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            user_profile=self.request.user.userprofile)
        return context


class OrderDetailsView(LoginRequiredMixin, TemplateView):
    """ Display the user's orders. """
    template_name = 'checkout/checkout_success.html'

    def get(self, request, order_number, *args, **kwargs):
        self.order = get_object_or_404(Order, order_number=order_number)
        return super().get(self, request, order_number, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['from_orders'] = True
        return context
