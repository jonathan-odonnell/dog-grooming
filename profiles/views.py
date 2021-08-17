from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from allauth.account.models import EmailAddress
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(LoginRequiredMixin, UpdateView):
    """ Display the user's profile. """
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/profile.html'
    google_api_key = settings.GOOGLE_API_KEY
    success_url = reverse_lazy('profile')

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_api_key'] = self.google_api_key
        return context

    def get(self, request, *args: str, **kwargs):
        self.initial = {'email_address': request.user.email}
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        current_email = EmailAddress.objects.get(user=self.request.user)
        new_email = self.request.POST['email_address']

        if current_email.email != new_email:
            current_email.change(self.request, new_email)

        messages.success(self.request, 'Profile updated successfully')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, 'Update failed. Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data(form=form))
