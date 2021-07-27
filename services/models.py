from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=254)
    size = models.CharField(max_length=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
