from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Image
from .forms import ImageForm


class GalleryView(CreateView):
    model = Image
    form_class = ImageForm
    queryset = Image.objects.all()
    context_object_name = 'images'
    template_name = 'gallery/gallery.html'
    success_url = reverse_lazy('gallery')

    def get(self, request):
        self.object = None
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object_list
        return context

    def form_valid(self, form):
        self.object_list = self.get_queryset()
        messages.success(self.request, 'Successfully added image!')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, 'Failed to add service. \
            Please ensure the form is valid.')
        return self.render_to_response(self.get_context_data())
