from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from ..models import Event
from invitee.models import Invitee
from .serializers import EventSerializer, FestListSerializer, EventUpdateFestPk, EventDetailSerializer
from rest_framework.permissions import IsAuthenticated

import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.template.loader import render_to_string
from django.conf import settings
from fest.models import FestModel

from django.core.mail import EmailMessage

from mimetypes import guess_type
from os.path import basename
import random
import string

class EventListCreateAPI(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = ['created_by__username']
    lookup_url_kwarg = ['org_name']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def list(self, request):
        eventqueryset = self.get_queryset().filter(created_by=request.user.pk, fest=None).exclude(removed=True)
        e_serializer = EventSerializer(eventqueryset, many=True).data
        
        fest_queryset = FestModel.objects.filter(user=request.user)
        f_serializer = FestListSerializer(fest_queryset, many=True).data
        
        return Response({"events": e_serializer, "fest":f_serializer})
    
    
    
# def add_event_instance(request):
#     """
#     data = {
#         'event': {
#             'id': 1,
#             'name': 'aprth',
#             'type': {
#                 'offline': [{'price': 123, "datetime": "12:10:10", 'place': 'us'}],
#                 'online': [{'price': 123, "datetime": "12:10:10", 'link': 'www.com'}]
#             }
#         }
#     }
#     """
#     json.loads(request.body)
    

class EventRetriveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field= "pk"
    
    
    def perform_update(self, serializer):
        if self.request.user == serializer.created_by:
            instance = serializer.save(created_by=self.request.user)
        
    def perform_destroy(self, instance):
        if self.request.user == instance.created_by:
            instance.removed = True
            instance.save()
     
@api_view(["POST"])   
def event_update_festPk(request):
    data = json.loads(request.body)
    e_pk = data["event_pk"]
    event_obj = Event.objects.get(pk=e_pk, created_by=request.user)
    
    f_pk = data["fest_pk"]
    fest_obj = FestModel.objects.get(pk=f_pk, user=request.user)
    
    if event_obj.fest:
        return Response({"error":404, "data":"event is already in a fest"})
    
    event_obj.fest = fest_obj
    event_obj.save()
        
    return Response({"error":0, "data":"ok"})
    


@api_view(["GET"])
def send_email_to_all(request, event_pk):
    print("heya in the task")
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
    # connection = mail.get_connection()
    # connection.open()
    invitees = [i for i in event_instance.invitees.all()]        
    all_mail = []  
    for invitee in invitees :
        invitee.save()
        if invitee.qr_code:
            template = render_to_string('invitee/email_template.html', {"extra_fields":''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)), 'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "organization_or_college":event_instance.organization_or_college, "unique_id": invitee.unique_id})
            invitee.sent_email = True
            invitee.save()
            subject = "Initation for: " + event_instance.event_name
            message = template
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [invitee.email]
       
            image = invitee.qr_code
    
            
            image.open()

            # email = EmailMessage("sub", "pub", "thakkar.parth782@gmail.com", ["parthishere1234@gmail.com"])
            email = EmailMessage(subject, message, email_from, recipient_list,)
            email.attach(basename(image.name),image.read(), guess_type(image.name)[0])
            email.send(fail_silently=False)
            all_mail.append(email)
            image.close()
            
       
  
    # connection.send_messages(all_mail)
    # connection.close()
    message = {"message": "done", "code": 200}
    return Response(message)
        
    
@api_view(["GET"]) 
@login_required
def send_email_to_remaining(request, event_pk):
    
    user = request.user
    event_instance = Event.objects.exclude(removed=True).prefetch_related("invitees").get(pk=event_pk, created_by=user)
    
    invitees = event_instance.invitees.all()
    # print(participant)
    
    for invitee in invitees :
        if invitee.qr_code and not invitee.sent_email:
            template = render_to_string('invitee/email_template.html', {'name': invitee.name, 'email':invitee.email, 'phone_number':invitee.phone_number, "event_name":event_instance.event_name, "event_date":event_instance.event_date, "about":event_instance.about, "created_by":event_instance.created_by, "organization_or_college":event_instance.organization_or_college})
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
    message = {"message": "done", "code": 200}
    return Response(message)