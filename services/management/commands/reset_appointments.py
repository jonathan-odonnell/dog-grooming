from django.core.management.base import BaseCommand
from services.models import Appointment
from django.utils.timezone import now, localtime


class Command(BaseCommand):
    help = 'Resets expired reserved appointments'

    def handle(self, *args, **options):
        current_time = localtime(now())
        appointments = Appointment.objects.filter(
            last_updated__gte=current_time).update(
            reserved=False, last_updated=None)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {appointments} appointments'))
