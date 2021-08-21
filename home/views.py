from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.conf import settings
import requests
import json


class HomeView(TemplateView):
    template_name = 'home/index.html'

    def post(self, request):
        url = 'https://api.sendgrid.com/v3/marketing/contacts'
        payload = json.dumps({'contacts': [{'email': request.POST['email']}]})
        headers = {
            'authorization': f'Bearer {settings.EMAIL_HOST_PASSWORD}',
            'content-type': 'application/json'
        }
        response = requests.request('PUT', url, data=payload, headers=headers)
        return HttpResponse(response)
