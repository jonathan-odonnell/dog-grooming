from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
