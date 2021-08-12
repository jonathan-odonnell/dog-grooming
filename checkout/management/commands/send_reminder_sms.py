from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.timezone import now, localdate
from django.conf import settings
from services.models import Appointment
from datetime import timedelta
from sms import send_sms


class Command(BaseCommand):
    help = 'Sends appointment reminder SMS messages'

    def handle(self, *args, **options):
        appointment_date = localdate(now()) + timedelta(days=1)
        appointments = Appointment.objects.filter(
            start_time__date=appointment_date, end_time__date=appointment_date
        )
        messages_sent = 0
        for appointment in appointments:
            message_body = render_to_string(
                'checkout/reminder_sms_messages/message_body.txt',
                {'appointment': appointment}
            )
            messages_sent += send_sms(
                message_body,
                settings. DEFAULT_FROM_SMS,
                appointment.order.phone_number,
            )
        self.stdout.write(self.style.SUCCESS(
            f'Successfully sent {messages_sent} SMS messages'))
