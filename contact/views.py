from django.shortcuts import HttpResponse
from django.views.generic.edit import CreateView
from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact.html'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            contact = form.save(commit=False)
            contact.user_profile = self.request.user.userprofile
            contact.save()
        else:
            form.save()
        return HttpResponse(status=200)
