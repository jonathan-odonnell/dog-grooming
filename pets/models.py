from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from profiles.models import UserProfile


class Breed(models.Model):
    class Meta:
        ordering = ('id',)

    sizes = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Extra Large', 'Extra Large'),
    ]

    name = models.CharField(max_length=50)
    size = models.CharField(max_length=20, choices=sizes)

    def __str__(self):
        return self.name

    def get_size(self):
        return self.size


class Pet(models.Model):
    class Meta:
        ordering = ('id',)

    genders = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    breed = models.ForeignKey(
        Breed, null=True, blank=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=10, choices=genders)
    colour = models.CharField(max_length=50)
    health = models.TextField(null=True, blank=True)
    behaviour = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    grooming_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Vet(models.Model):
    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Vet'

    pet = models.OneToOneField(Pet, on_delete=models.CASCADE,
                            related_name='vet')
    full_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(max_length=20)
    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80)
    postcode = models.CharField(max_length=20)
    country = CountryField(blank_label='Country *')

    def __str__(self):
        return self.full_name


class EmergencyContact(models.Model):
    class Meta:
        ordering = ('id',)

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE,
                            related_name='emergency_contact')
    full_name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=20)
    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80)
    postcode = models.CharField(max_length=20)
    country = CountryField(blank_label='Country *')

    def __str__(self):
        return self.full_name
