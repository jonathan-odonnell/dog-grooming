from django.contrib import admin
from .models import Pet, Breed


class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'size',)
    list_filter = ('size',)
    list_per_page = 20


admin.site.register(Breed, BreedAdmin)
admin.site.register(Pet)
