from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Service, BusinessHour
from checkout.models import Appointment
from .forms import ServiceForm
from .utils import SuperUserRequired
from datetime import datetime, date, timedelta
import calendar
from calendar import Calendar


class ServicesView(ListView):
    model = Service
    template_name = 'services/services.html'


class AppointmentsView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'services/appointments.html'
    context_object_name = 'service'

    def get_context_data(self, month=None, year=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not month:
            current_date = date.today()
            month = current_date.month
            year = current_date.year
        context['calendar'] = Calendar(6).monthdayscalendar(year, month)
        context['month'] = calendar.month_name[month]
        context['year'] = year
        return context

    def get(self, request, pk, month=None, year=None):
        self.object = self.get_object()
        context = self.get_context_data(month, year)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'calendar': context['calendar'],
                'month': context['month'],
                'year': context['year'],
            })
        else:
            return self.render_to_response(context)

    def post(self, request, pk):
        date = datetime.strptime(
            request.POST['date'], '%d/%m/%Y').replace(
                tzinfo=timezone.get_current_timezone())
        business_hours = BusinessHour.objects.get(
            start_date__lte=date, end_date__gte=date)
        appointments = ['10:00', '13:00', '15:00']
        appointments_start = datetime.combine(
            date, business_hours.start_time).replace(
            tzinfo=timezone.get_current_timezone())
        appointments_end = datetime.combine(
            date, business_hours.end_time).replace(
            tzinfo=timezone.get_current_timezone())
        booked_appointments = Appointment.objects.filter(
            start__gte=appointments_start,
            end__lte=appointments_end
        )

        for appointment in appointments:
            appointment_start = datetime.strptime(appointment, '%H:%M').time()
            appointment_end = (datetime.strptime(
                appointment, '%H:%M') + timedelta(hours=2)).time()
            if (appointment_start <= business_hours.start_time
                    or appointment_end > business_hours.end_time):
                appointments.remove(appointment)

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
