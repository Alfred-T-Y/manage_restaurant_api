from celery import shared_task
from django.core.mail import EmailMessage
from twilio.rest import Client
import dotenv
import os



@shared_task
def send_email(data):

    email = EmailMessage(
        subject=data['email_subject'], 
        body=data['email_body'], to=[data['to_email']]
        )
    email.send()


@shared_task
def send_sms(data):

    client = Client(
        os.getenv('TWILIO_SID'), 
        os.getenv('TWILIO_TOKEN'))

    message = client.messages.create(
        body= data['message'],
        from_= os.getenv('TWILIO_PHONENUMBER'),
        to= data['to']
    )