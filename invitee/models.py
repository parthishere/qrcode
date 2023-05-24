
from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_qrcode
User = get_user_model()
from django.db.models.signals import pre_save, post_save

import random
import string


def random_string_generator(size=7, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
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
class Invitee(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_all_invitees")
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100, blank=True)
    # event = models.ForeignKey("events.Event", on_delete=models.CASCADE, null=True, related_name="event_invitees")
    email = models.EmailField()
    phone_number = models.BigIntegerField()
    other_info = models.TextField()
    recognized = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to=f"media/invitees/", blank=True)
    pass_template = models.ImageField(upload_to=f"media/{created_by}/invitees_pass/", blank=True)
    sent_email = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name + " created by: " + self.created_by.username
    
    def save(self, *args, **kwargs):
        
        try:
            self.qr_code.delete(save=False)
        except:
            pass

        if not self.qr_code:
            # Generate QR code if it doesn't exist
            data_to_encode = f"{self.name},{self.email},{self.phone_number},{self.event.pk},{self.unique_id}"
            filename = f"{self.name}_{self.unique_id}_qr.png"
            qr_code_image = generate_qrcode(data_to_encode, filename)
            self.qr_code.save(qr_code_image.name, qr_code_image, save=False)
        super().save(*args, **kwargs)
        
  
    
def invitee_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.unique_id == None or instance.unique_id == "" or instance.pk=="" or instance.pk==None:
        print("ohk")
        instance.unique_id = unique_id_generator(instance)
            

pre_save.connect(invitee_pre_save_receiver, sender=Invitee)