from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            contact = form.save(commit=False)
            contact.user_profile = self.request.user.userprofile
            contact.save()
        else:
            form.save()
        return redirect(self.get_success_url())
