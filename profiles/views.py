from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from .models import UserProfile, Pet
from checkout.models import Order
from .forms import UserProfileForm, PetForm


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
        self.object.user.email = self.request.POST['email_address']
        self.object.user.save()
        messages.success(self.request, 'Profile updated successfully')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, 'Update failed. Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data(form=form))


class OrdersView(LoginRequiredMixin, ListView):
    """ Display the user's orders. """
    context_object_name = 'orders'
    template_name = 'profiles/orders.html'

    def get_queryset(self):
        return Order.objects.filter(
            user_profile=self.request.user.userprofile)


class OrderDetailsView(LoginRequiredMixin, DetailView):
    """ Displays the user's orders. """
    context_object_name = 'order'
    template_name = 'checkout/checkout_success.html'

    def get_object(self):
        return get_object_or_404(
            Order, order_number=self.kwargs['order_number'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['from_orders'] = True
        return context


class PetsView(LoginRequiredMixin, ListView):
    """ Displays the user's pets. """
    context_object_name = 'pets'
    template_name = 'profiles/pets.html'

    def get_queryset(self):
        return Pet.objects.filter(
            user_profile=self.request.user.userprofile)


class AddPetView(LoginRequiredMixin, CreateView):
    """ Adds a pet """
    form_class = PetForm
    template_name = 'profiles/add_pet.html'
    success_url = reverse_lazy('pets')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_profile = self.request.user.userprofile
        self.object.save()
        messages.success(self.request, 'Successfully added pet!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update pet. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())


class EditPetView(LoginRequiredMixin, UpdateView):
    """ Edits a pet """
    form_class = PetForm
    context_object_name = 'pet'
    template_name = 'profiles/edit_pet.html'
    success_url = reverse_lazy('pets')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_profile = self.request.user.userprofile
        self.object.save()
        messages.success(self.request, 'Successfully updated pet!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update pet. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())


class DeletePetView(LoginRequiredMixin, DeleteView):
    """ Deletes the pet """
    http_method_names = ['get']
    form_class = PetForm
    success_url = reverse_lazy('pets')

    def get(self, request, pk):
        self.object.delete()
        messages.success(request, 'Successfully deleted pet!')
        return redirect(self.get_success_url())
