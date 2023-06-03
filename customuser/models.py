from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import pre_save, post_save

import random
import string

# Create your models here.
  
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
        new_slug = "{randstr}".format(
                    randstr=random_string_generator(size=12)
                )
        return new_slug
    else:
        return new_id

class CustomUser(AbstractUser):
    is_pro = models.BooleanField(default=False)
    phonenumber = models.IntegerField(default=9999999)
    is_updated = models.BooleanField(default=False)
    unique_id = models.CharField(max_length=12, null=True, blank=True)
    

def customuser_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.unique_id == None or instance.unique_id == "" or instance.pk==None:
        instance.unique_id = unique_id_generator(instance)
            

pre_save.connect(customuser_pre_save_receiver, sender=CustomUser)