from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission
from .models import UserProfile
from pets.models import Pet


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile and adds permissions
    if user has been created
    """
    if created:
        if instance.is_superuser:
            permissions = Permission.objects.all()
            instance.user_permissions.set(permissions)
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


@receiver(post_save, sender=UserProfile)
def update_emergency_contacts(sender, instance, created, **kwargs):
    """
    Update the emergency contact details if the user profile
    has been updated
    """
    if not created:
        pets = Pet.objects.filter(
            user_profile=instance, emergency_contacts__relationship='Owner')
        for pet in pets:
            pet.emergency_contacts.update(
                phone_number=instance.phone_number,
                address_line_1=instance.address_line_1,
                address_line_2=instance.address_line_2,
                town_or_city=instance.town_or_city,
                county=instance.county,
                postcode=instance.postcode,
                country=instance.country
            )
