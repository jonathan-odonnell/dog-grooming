from django.views.generic.base import TemplateView
from django.shortcuts import HttpResponse
from .models import NewsletterEmail


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def post(self, request):
        NewsletterEmail.objects.create(email=request.POST['newsletter'])
        return HttpResponse(status=200)

