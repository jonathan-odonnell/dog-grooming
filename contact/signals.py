from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Contact


@receiver(post_save, sender=Contact)
def send_email_on_save(sender, instance, created, **kwargs):
    """
    Sends email when a new customer contact is saved
    """
    if created:
        admin_email = settings.DEFAULT_FROM_EMAIL
        subject = render_to_string(
            'contact/emails/subject.txt',
            {'contact': instance})
        body = render_to_string(
            'contact/emails/body.txt',
            {'contact': instance})
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [admin_email]
        )
