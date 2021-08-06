from django.db import models
from django.db.models.deletion import CASCADE


class Service(models.Model):
    name = models.CharField(max_length=254)
    image = models.ImageField()
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Price(models.Model):
    CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    service = models.ForeignKey(
        Service, on_delete=CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=2, choices=CHOICES)

    def __str__(self):
        return f'{self.price} - {self.size}'


class Availability(models.Model):
    class Meta:
        verbose_name_plural = "Availability"

    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'
