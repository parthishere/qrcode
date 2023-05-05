import tempfile
import string
import random
from events.models import Event
from celery import shared_task
from django.template.loader import render_to_string

from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.contenttypes.models import ContentType

@shared_task
def send_email_to_all(extra_fields, request, event_pk):
    print("heya in the task")
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
   
    invitees = [i for i in event_instance.invitees.all()]        
        
    for invitee in invitees :
        invitee.save()
        if invitee.qr_code:
            template = render_to_string('app/email_template.html', {"extra_fields":''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)), 'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "organization_or_college":event_instance.organization_or_college})
            invitee.sent_email = True
            invitee.save()
            subject = "Initation for: " + event_instance.event_name
            message = template
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invitee.email]
       
            image_file = invitee.qr_code

           

            mail = EmailMessage(subject, message, email_from, recipient_list)
            mail.attach("image.png", image_file.read(), "image/jpg")
        
            mail.send()
            print("email sent")
       
    # group_name = get_user_name()  # Find out way to get same as what is printed on connect()

    # channel_layer = get_channel_layer()
    # # Trigger reload message sent to group
    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {'type': 'reload_page'}
    # )
    return None
        
    
@shared_task
def send_email_to_remaining(extra_fields, request, event_pk):
    
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
    invitees = event_instance.invitees.all()
    # print(participant)
    
    for invitee in invitees :
        if invitee.qr_code and not invitee.sent_email:
            template = render_to_string('app/email_template.html', {"extra_fields":extra_fields, 'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "organization_or_college":event_instance.organization_or_college})
            invitee.sent_email = True
            invitee.save()
            subject = "Initation for: " + event_instance.event_name
            message = template
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invitee.email,]
            mail = EmailMessage(subject, message, email_from, recipient_list)
            mail.attach(invitee.qr_code.name, invitee.qr_code.read())
            mail.send()
       
    # group_name = get_user_name()  # Find out way to get same as what is printed on connect()

    # channel_layer = get_channel_layer()
    # # Trigger reload message sent to group
    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {'type': 'reload_page'}
    # )
    return None