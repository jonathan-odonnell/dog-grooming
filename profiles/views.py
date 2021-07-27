from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


class ProfileView(View):
    """ Display the user's profile. """

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/profile.html'

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class(initial={'email_address': request.user.email})
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            profile = form.save()
            profile.user.email = request.POST['email_address']
            profile.user.save()
            messages.success(request, 'Profile updated successfully')

        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.')

        return render(request, self.template_name, {'form': form})
