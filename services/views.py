from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Min
from django.utils.timezone import make_aware
from .models import Service, Appointment
from .forms import ServiceForm, PriceFormSet
from .utils import SuperUserRequired
from datetime import datetime, date
import calendar
from calendar import Calendar


class ServicesView(ListView):
    queryset = Service.objects.annotate(price=Min('prices__price'))
    context_object_name = 'services'
    template_name = 'services/services.html'


class AppointmentsView(LoginRequiredMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'services/appointments.html'

    def get_context_data(self, month=None, year=None, **kwargs):
        context = super().get_context_data(**kwargs)
        day = 1

        if not month:
            current_date = date.today()
            day = current_date.day + 1
            month = current_date.month
            year = current_date.year

        num_days = calendar.monthrange(year, month)[1]
        classes = []

        for i in range(1, num_days + 1):
            day_date = date(year, month, i)
            appointments = self.get_appointments(day_date)
            if i >= day and len(appointments) == 1:
                classes.append('availability-1')
            elif i >= day and len(appointments) == 2:
                classes.append('availability-2')
            elif i >= day and len(appointments) == 3:
                classes.append('availability-3')
            else:
                classes.append('disabled')

        context['calendar'] = Calendar(6).monthdayscalendar(year, month)
        context['classes'] = classes
        context['month'] = calendar.month_name[month]
        context['year'] = year
        return context

    def get_appointments(self, date):
        available_appointments = []
        appointments = Appointment.objects.filter(
            start__date__gte=date, end__date__lte=date, order=None)
        for appointment in appointments:
            available_appointments.append(appointment.start.strftime('%H:%M'))
        return available_appointments

    def get(self, request, pk, month=None, year=None):
        self.object = self.get_object()
        context = self.get_context_data(month, year)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'calendar': context['calendar'],
                'classes': context['classes'],
                'month': context['month'],
                'year': context['year'],
            })
        else:
            return self.render_to_response(context)

    def post(self, request, pk):
        date = make_aware(datetime.strptime(
            request.POST['date'], '%d/%m/%Y'))
        appointments = self.get_appointments(date)
        return JsonResponse({'appointments': appointments})


class AddServiceView(LoginRequiredMixin, SuperUserRequired, CreateView):
    model = Service
    form_class = ServiceForm
    context_object_name = 'service'
    template_name = 'services/add_service.html'
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PriceFormSet(self.request.POST)
        else:
            context['formset'] = PriceFormSet()
        return context

    def form_valid(self, form):
        self.object = form.save()
        formset = PriceFormSet(self.request.POST, instance=form)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'Successfully added service!')
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(formset)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to add service. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())


class EditServiceView(LoginRequiredMixin, SuperUserRequired, UpdateView):
    model = Service
    form_class = ServiceForm
    context_object_name = 'service'
    template_name = 'services/edit_service.html'
    success_url = reverse_lazy('services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PriceFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = PriceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save()
        formset = PriceFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
            messages.success(self.request, 'Successfully updated service!')
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(formset)

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update service. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())


class DeleteServiceView(LoginRequiredMixin, SuperUserRequired, DeleteView):
    model = Service
    success_url = reverse_lazy('services')
    http_method_names = ['POST']

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, 'Successfully deleted service!')
        return redirect(self.get_success_url())
