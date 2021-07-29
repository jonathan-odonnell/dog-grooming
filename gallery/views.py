from django.views.generic.base import TemplateView


class GalleryView(TemplateView):
    template_name = 'gallery/gallery.html'
