from django.core.management.base import BaseCommand
from services.models import Appointment
from django.utils.timezone import now, localtime
from datetime import timedelta


class Command(BaseCommand):
    help = 'Resets expired reserved appointments'

    def handle(self, *args, **options):
        removal_time = localtime(now()) - timedelta(days=1)
        appointments = Appointment.objects.filter(
            last_updated__lte=removal_time).update(
            reserved=False, last_updated=None)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {appointments} appointments'))
