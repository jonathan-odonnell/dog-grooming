from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(LoginRequiredMixin, View):
    """ Display the user's profile. """

    form_class = UserProfileForm
    template_name = 'profiles/profile.html'

    def get(self, request):
        form = self.form_class(initial={'email_address': request.user.email})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = self.form_class(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save()
            profile.user.email = request.POST['email_address']
            profile.user.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')

        return render(request, self.template_name, {'form': form})
