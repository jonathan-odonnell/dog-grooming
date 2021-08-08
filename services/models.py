from django.db import models
from django.utils.timezone import get_current_timezone


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
        Service, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=2, choices=CHOICES)

    def __str__(self):
        return f'{self.price} - {self.size}'


class Availability(models.Model):
    class Meta:
        verbose_name_plural = "Availability"

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def convert_to_localtime(self, utctime):
        fmt = '%d/%m/%Y %H:%M'
        localtz = utctime.astimezone(get_current_timezone())
        return localtz.strftime(fmt)

    def __str__(self):
        return f'{self.convert_to_localtime(self.start_time)} - \
            {self.convert_to_localtime(self.end_time)}'


class Appointment(models.Model):
    order = models.ForeignKey('checkout.Order', on_delete=models.CASCADE,
                              null=True, blank=True,
                              related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    comments = models.TextField(null=True, blank=True)
    reserved = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    def convert_to_localtime(self, utctime):
        fmt = '%d/%m/%Y %H:%M'
        localtz = utctime.astimezone(get_current_timezone())
        return localtz.strftime(fmt)

    def __str__(self):
        return f'{self.convert_to_localtime(self.start)} - \
            {self.convert_to_localtime(self.end)}'
