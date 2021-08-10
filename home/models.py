from django.db import models


class NewsletterEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
