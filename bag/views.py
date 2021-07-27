from django.views.generic.base import View, TemplateView


class BagView(TemplateView):
    template_name = "bag/bag.html"
