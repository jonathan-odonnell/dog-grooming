from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Service
from .forms import ServiceForm
from .utils import SuperUserRequired


class ListServicesView(ListView):
    model = Service
    template_name = 'services/services.html'


class ListPricesView(ListView):
    model = Service
    template_name = 'services/prices.html'


class AddServiceView(LoginRequiredMixin, SuperUserRequired, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Successfully added service!')
        else:
            messages.error(
                request, 'Failed to add service. \
                    Please ensure the form is valid.')
        return super().post(request, *args, **kwargs)


class EditServiceView(LoginRequiredMixin, SuperUserRequired, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/edit_service.html'
    success_url = reverse_lazy('services')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Successfully updated service!')
        else:
            messages.error(request, 'Failed to update service. \
                Please ensure the form is valid.')
        return super().post(request, *args, **kwargs)


class DeleteServiceView(LoginRequiredMixin, SuperUserRequired, DeleteView):
    model = Service
    success_url = reverse_lazy('services')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'Successfully deleted service!')
        return super().post(request, *args, **kwargs)
