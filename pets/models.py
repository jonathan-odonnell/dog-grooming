from django.db import models
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

    def __str__(self):
        return self.name
