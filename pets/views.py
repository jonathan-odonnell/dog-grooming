from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_countries.fields import country_to_text
from .models import Pet
from .forms import PetForm


class PetsView(LoginRequiredMixin, ListView):
    """ Displays the user's pets. """
    context_object_name = 'pets'
    template_name = 'pets/pets.html'

    def get_queryset(self):
        return Pet.objects.filter(
            user_profile=self.request.user.userprofile)


class AddPetView(LoginRequiredMixin, CreateView):
    """ Adds a pet """
    model = Pet
    form_class = PetForm
    template_name = 'pets/add_pet.html'
    success_url = reverse_lazy('pets')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_profile = self.request.user.userprofile
        self.object.save()
        self.object.emergency_contacts.create(
            full_name=self.request.user.userprofile.user.get_full_name(),
            relationship='Owner',
            phone_number=self.request.user.userprofile.phone_number,
            address_line_1=self.request.user.userprofile.address_line_1,
            address_line_2=self.request.user.userprofile.address_line_2,
            town_or_city=self.request.user.userprofile.town_or_city,
            county=self.request.user.userprofile.county,
            postcode=self.request.user.userprofile.postcode,
            country=self.request.user.userprofile.country
        )
        messages.success(self.request, 'Successfully added pet!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update pet. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())


class EditPetView(LoginRequiredMixin, UpdateView):
    """ Edits a pet """
    model = Pet
    form_class = PetForm
    context_object_name = 'pet'
    template_name = 'pets/edit_pet.html'
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
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy('pets')

    def get(self, request, pk):
        self.object.delete()
        messages.success(request, 'Successfully deleted pet!')
        return redirect(self.get_success_url())
