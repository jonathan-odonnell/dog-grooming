from django.shortcuts import get_object_or_404
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order


class OrdersView(LoginRequiredMixin, ListView):
    """ Display the user's orders. """
    template_name = 'orders/orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(
            user_profile=self.request.user.userprofile).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = context['page_obj']
        del context['page_obj']
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context = self.get_context_data()
            orders = render_to_string(
                'orders/orders-table.html', context, request)
            return JsonResponse({'orders': orders})
        else:
            return super().get(request, *args, **kwargs)


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
