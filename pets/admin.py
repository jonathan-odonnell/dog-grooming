from django.contrib import admin
from .models import Pet, Breed


class BreedAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('name', 'dog_size',)
    list_filter = ('dog_size',)
    list_per_page = 20


admin.site.register(Breed, BreedAdmin)
admin.site.register(Pet)
