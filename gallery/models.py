from django.db import models


class Image(models.Model):
    class Meta:
        ordering = ('id',)

    name = models.CharField(max_length=254)
    image = models.ImageField()

    def __str__(self):
        return self.name
