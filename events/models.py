from datetime import datetime
from enum import unique
from django.shortcuts import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
User = get_user_model()
from django.db.models.signals import pre_save, post_save

import random
import string

from datePrice.models import VirtualModel, OfflineModel


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_id_generator(instance):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    new_id = random_string_generator(size=12)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_id=new_id).exists()
    if qs_exists:
        unique_id_generator(instance)
    else:
        return new_id


# Create your models here.
class Event(models.Model):
    unique_id = models.CharField(max_length=20)
    organization_or_college = models.CharField(max_length=120, null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    moderators = models.ManyToManyField(User, blank=True, related_name="events_as_moderator")
    event_name = models.CharField(max_length=100)
    
    about = models.TextField(null=True)
    contact_number = models.IntegerField(null=True,blank=True)
    contact_email = models.EmailField(null=True,blank=True)
    contact_number_2 = models.IntegerField(null=True, blank=True)
    contact_email_2 = models.EmailField(null=True, blank=True)
    instance_created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    online_events = models.ManyToManyField(VirtualModel, blank=True, null=True, related_name="all_online_events")
    offline_events = models.ManyToManyField(OfflineModel, blank=True,null=True, related_name="all_online_events")
    invitees = models.ManyToManyField("invitee.Invitee", blank=True, related_name="all_events")
    recognized_invitees = models.ManyToManyField("invitee.Invitee", blank=True, related_name="attended_all_events")
    fast_check = models.BooleanField(default=True)
    pass_template = models.ImageField(upload_to=f"media/{created_by}/events/", null=True, blank=True)
    qr_code_coordinate_x = models.FloatField(null=True)
    qr_code_coordinate_y = models.FloatField(null=True)
    name_coordinate_x = models.FloatField(null=True)
    name_coordinate_y = models.FloatField(null=True)
    pre_define_pass =models.BooleanField(default=False)
    predefined_pass_image = models.ImageField(null=True, blank=True)
    event_update_count = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)
    fest = models.ForeignKey("fest.FestModel",on_delete=models.CASCADE, null=True, blank=True, related_name="events")

    
    class Meta():
        unique_together = ("created_by", "event_name")
    
    def __str__(self):
        return self.event_name +" created by: "+self.created_by.username
    
    @property
    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})
    
    
def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.unique_id == None or instance.unique_id == "" or instance.pk==None:
        instance.unique_id = unique_id_generator(instance)
            

pre_save.connect(event_pre_save_receiver, sender=Event)
    