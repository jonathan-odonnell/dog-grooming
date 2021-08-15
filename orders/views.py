from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order


class OrdersView(LoginRequiredMixin, ListView):
    """ Display the user's orders. """
    context_object_name = 'orders'
    template_name = 'profiles/orders.html'

    def get_queryset(self):
        return Order.objects.filter(
            user_profile=self.request.user.userprofile).order_by('-date')


class OrderDetailsView(LoginRequiredMixin, DetailView):
    """ Displays the user's orders. """
    context_object_name = 'order'
    template_name = 'checkout/checkout_success.html'

    def get_object(self):
        return get_object_or_404(
            Order, order_number=self.kwargs['order_number'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_orders'] = True
        return context
