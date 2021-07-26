from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    billing information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=20)
    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40)
    county = models.CharField(max_length=80)
    postcode = models.CharField(max_length=20)
    country = CountryField(blank_label='Country *')

    def __str__(self):
        return self.user.username
