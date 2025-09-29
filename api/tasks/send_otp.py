from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_otp_email(email, otp_code):
    subject = "Your OTP Code - Lead Magnet"
    message = f"Hello,\n\nYour OTP code is: {otp_code}\nIt is valid for 10 minutes.\n\nThank you,\nLead Magnet Team"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
    return f"OTP sent to {email}"
