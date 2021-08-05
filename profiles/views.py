from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from .models import UserProfile
from checkout.models import Order
from .forms import UserProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    """ Display the user's profile. """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/profile.html'
    google_api_key = settings.GOOGLE_API_KEY
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = settings.GOOGLE_API_KEY
        return context

    def get(self, request, *args: str, **kwargs):
        self.initial = {'email_address': request.user.email}
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        self.object.user.email = self.request.POST['email_address']
        self.object.user.save()
        messages.success(self.request, 'Profile updated successfully')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, 'Update failed. Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data(form=form))


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
