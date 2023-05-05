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
import accounts.models


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
    organization_or_college = models.CharField(max_length=120, default="LD college")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    moderators = models.ManyToManyField(User, blank=True, related_name="events_as_moderator")
    event_name = models.CharField(max_length=100)
    event_date = models.DateTimeField(default=now)
    venue = models.CharField(max_length=120, null=True)
    about = models.TextField(null=True)
    contact_number = models.IntegerField(default="999999999")
    contact_email = models.EmailField(default="info@allevents.com")
    contact_number_2 = models.IntegerField(null=True, blank=True)
    contact_email_2 = models.EmailField(null=True, blank=True)
    instance_created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    invitees = models.ManyToManyField("accounts.Invitee", blank=True, related_name="all_events")
    recognized_invitees = models.ManyToManyField("accounts.Invitee", blank=True, related_name="attended_all_events")
    fast_check = models.BooleanField(default=True)
    pass_template = models.ImageField(upload_to=f"media/{created_by}/events/", null=True, blank=True)
    name_coordinates = models.BooleanField(default=False)
    event_coordinates = models.BooleanField(default=False)
    qr_code_coordinates = models.TextField()
    name_coordinates = models.TextField()
    pre_define_pass =models.BooleanField(default=False)
    predefined_pass_image = models.ImageField(null=True, blank=True)
    event_update_count = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)

    
    class Meta():
        unique_together = ("created_by", "unique_id")
    
    def __str__(self):
        return self.event_name +" created by: "+self.created_by.username
    
    @property
    def get_absolute_url(self):
        return reverse("events:detail", kwargs={"pk": self.pk})
    
    
def event_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.unique_id == None or instance.unique_id == "" or instance.pk==None:
        instance.unique_id = unique_id_generator(instance)
            

pre_save.connect(event_pre_save_receiver, sender=Event)
    