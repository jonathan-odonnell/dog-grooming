from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Service
from checkout.models import Appointment
from .forms import ServiceForm
from .utils import SuperUserRequired
from datetime import datetime


class ServicesView(ListView):
    model = Service
    template_name = 'services/services.html'


class AppointmentsView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'services/appointments.html'
    context_object_name = 'service'

    def post(self, request, pk):
        start = datetime.strptime(
            request.POST['date'], '%d/%m/%Y').replace(
                tzinfo=timezone.get_current_timezone())
        end = start.replace(hour=18)
        appointments = ['10:00', '13:00', '15:00']
        booked_appointments = Appointment.objects.filter(
            start__gte=start, end__lte=end)
        print(booked_appointments)

        for appointment in booked_appointments:
            appointment = timezone.localtime(
                appointment.start, timezone.get_current_timezone()
                ).strftime('%H:%M')
            if appointment in appointments:
                appointments.remove(appointment)

        return JsonResponse({'appointments': appointments})


class AddServiceView(LoginRequiredMixin, SuperUserRequired, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully added service!')
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to add service. \
            Please ensure the form is valid.')
        return render(self.request,
                      self.template_name, self.get_context_data())


class EditServiceView(LoginRequiredMixin, SuperUserRequired, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'services/edit_service.html'
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully updated service!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update service. \
            Please ensure the form is valid.')
        return render(self.request,
                      self.template_name, self.get_context_data())


class DeleteServiceView(LoginRequiredMixin, SuperUserRequired, DeleteView):
    model = Service
    success_url = reverse_lazy('services')
    http_method_names = ['POST']

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, 'Successfully deleted service!')
        return redirect(self.get_success_url())
