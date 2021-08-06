from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=254)
    image = models.ImageField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BusinessHour(models.Model):
    class Meta:
        verbose_name = "Business Hours"
        verbose_name_plural = "Business Hours"

    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'
