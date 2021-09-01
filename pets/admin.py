from django.contrib import admin
from .models import Pet, Breed, Vet, EmergencyContact


class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'size',)
    list_filter = ('size',)
    list_per_page = 20


class EmergencyContactAdminInline(admin.StackedInline):
    model = EmergencyContact
    extra = 1
    max_num = 2
    classes = ['collapse']


class VetAdminInline(admin.StackedInline):
    model = Vet
    extra = 1
    max_num = 1
    classes = ['collapse']


class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'date_of_birth', 'colour',)
    list_per_page = 20
    inlines = [EmergencyContactAdminInline, VetAdminInline]


admin.site.register(Breed, BreedAdmin)
admin.site.register(Pet, PetAdmin)
