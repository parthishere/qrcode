from PIL import Image
from io import BytesIO
import string
import random
from events.models import Event
from qrwebsite.celery import app
from celery import shared_task
from django.template.loader import render_to_string

from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.core import mail
from django.conf import settings
from qrwebsite.celery import app
from django.contrib.auth import get_user_model

User = get_user_model()

from mimetypes import guess_type
from os.path import basename

from django.core.files.storage import get_storage_class

media_storage = get_storage_class()()

@app.task
def send_email_to_all(extra_fields, request, event_pk):
    print("heya in the task")
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
    # connection = mail.get_connection()
    # connection.open()
    invitees = [i for i in event_instance.invitees.all()]   
    total_count = event_instance.invitees.all().count()     
    all_mail = []  
    htmly   = get_template('app/email_template.html')
    for invitee in invitees :
        
        invitee.save()
        if invitee.qr_code:
            boto_s3_url = media_storage.url(name=invitee.qr_code.file.name)
            
            context = {"extra_fields":''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)), 'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "fileurl":boto_s3_url}
            
            html_content = htmly.render(context)
            
            template = render_to_string('app/email_template.html', context)
            invitee.sent_email = True
            invitee.save()
            subject = "Initation for: " + event_instance.event_name
            message = template
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invitee.email]
       
            image = invitee.qr_code
    
            
            image.open()

            # email = EmailMessage("sub", "pub", "thakkar.parth782@gmail.com", ["parthishere1234@gmail.com"])
            email = EmailMultiAlternatives(subject, message, email_from, recipient_list,)
            email.attach_alternative(html_content, "text/html")
            email.attach(basename(image.name),image.read(), guess_type(image.name)[0])
            email.send(fail_silently=False)
            all_mail.append(email)
            image.close()
            print("email sent to "+ invitee.name +" on email: "+ invitee.email + " count :", invitees.index(invitee)+1, " total count: ", total_count)
            
       
  
    # connection.send_messages(all_mail)
    # connection.close()
    return None
        
    
@app.task
def send_email_to_remaining(extra_fields, request, event_pk):
    
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
    invitees = event_instance.invitees.all()
    # print(participant)
    htmly   = get_template('app/email_template.html')
    for invitee in invitees :
        if invitee.qr_code and not invitee.sent_email:
            boto_s3_url = media_storage.url(name=invitee.qr_code.file.name)
            
            context = {"extra_fields":''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)), 'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "fileurl":boto_s3_url}
            
            html_content = htmly.render(context)
            
            template = render_to_string('app/email_template.html', context)
            invitee.sent_email = True
            invitee.save()
            subject = "Initation for: " + event_instance.event_name
            message = template
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invitee.email]
       
            image = invitee.qr_code
    
            
            image.open()

            # email = EmailMessage("sub", "pub", "thakkar.parth782@gmail.com", ["parthishere1234@gmail.com"])
            email = EmailMultiAlternatives(subject, message, email_from, recipient_list,)
            email.attach_alternative(html_content, "text/html")
            email.attach(basename(image.name),image.read(), guess_type(image.name)[0])
            email.send(fail_silently=False)
            
            image.close()
            print("email sent to "+ invitee.name +" on email: "+ invitee.email + " count :", invitees.index(invitee)+1)
    # group_name = get_user_name()  # Find out way to get same as what is printed on connect()

    # channel_layer = get_channel_layer()
    # # Trigger reload message sent to group
    # async_to_sync(channel_layer.group_send)(
    #     group_name,
    #     {'type': 'reload_page'}
    # )
    return None