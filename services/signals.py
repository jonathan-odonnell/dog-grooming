from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from .models import Availability
from datetime import datetime, timedelta
from checkout.models import Appointment


@receiver(pre_save, sender=Availability)
@receiver(pre_delete, sender=Availability)
def delete_appointments_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    availability = Availability.objects.get(id=instance.id)
    Appointment.objects.filter(
        start__gte=availability.end_time,
        end__lte=availability.end_time,
        order=None
    ).delete()


@receiver(post_save, sender=Availability)
def add_appointments_on_save(sender, instance, **kwargs):
    """
    Update order total on lineitem update/create
    """
    appointments = ['10:00', '13:00', '15:00']
    time_delta = instance.end_time - instance.start_time

    for i in range(time_delta.days + 1):
        date = instance.start_time.date() + timedelta(days=i)
        for appointment in appointments:
            start_time = datetime.combine(date, datetime.strptime(
                appointment, '%H:%M').time())
            end_time = datetime.combine(date, datetime.strptime(
                appointment, '%H:%M').time()) + timedelta(hours=2)
            # Appointment.objects.create(start=start_time, end=end_time)
