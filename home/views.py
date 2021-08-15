from django.views.generic.base import TemplateView
from django.views.generic import FormView
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import NewsletterEmail
from .forms import NewsletterEmailForm
from services.utils import SuperUserRequiredMixin


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def post(self, request):
        NewsletterEmail.objects.create(email=request.POST['newsletter'])
        return HttpResponse(status=200)


class NewsletterEmailView(SuperUserRequiredMixin, FormView):
    form_class = NewsletterEmailForm
    template_name = 'home/newsletter-email.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super().form_valid(form)

    def send_mail(self, form_data):
        email_list = NewsletterEmail.objects.values_list('email', flat=True)
        send_mass_mail(
            form_data['subject'],
            form_data['message'],
            settings.DEFAULT_FROM_EMAIL,
            [email_list]
        )
