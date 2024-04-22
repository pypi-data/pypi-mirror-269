# myapp/utils.py

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from doctor.models import Appointment
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime

def send():
    return "hello world............"

def email_me(first_name,date,email):
        data = {
            "fname":first_name,
            "date":date,
        }

        message = render_to_string('email.html', data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email.content_subtype = "html"
        email.send()

def enquiry(email,message):
        email = EmailMessage(
        subject= f"General enquiry regarding doctors availabilty.",
        body=message,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER],
        reply_to=[email]
    )
        email.send()
