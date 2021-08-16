from django.template.loader import render_to_string
from django.conf import settings
from .models import Appointment
from sms import send_sms
import dramatiq


@dramatiq.actor
def send_sms_reminder(appointment_id):
    """Send a SMS appointment reminder"""
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return

    message_body = render_to_string(
        'checkout/reminder_sms_messages/message_body.txt',
        {'appointment': appointment}
    )
    send_sms(
        message_body,
        settings. DEFAULT_FROM_SMS,
        appointment.order.phone_number,
    )
