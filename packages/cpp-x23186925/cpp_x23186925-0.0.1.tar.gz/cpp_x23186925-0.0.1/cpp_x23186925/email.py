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

def email_me(message,host,email):

        #message = render_to_string('email.html', data)
        email = EmailMessage(
            "About your appointment",
            message,
            host,
            [email],
        )
        email.content_subtype = "html"
        email.send()

def enquiry(subject,email_from,message,to):
        email = EmailMessage(
        subject= subject,
        body=message,
        from_email=email_from,
        to=[to]
    )
        email.send()


