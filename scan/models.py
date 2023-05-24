from django.db import models
from django.core.validators import MaxValueValidator
from io import BytesIO
import qrcode 
from django.core.files import File
from PIL import Image, ImageDraw
import os
from django.utils.text import slugify

from .utils import random_string_generator
from django.db.models.signals import post_save, pre_save


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name, instance.email)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


# Create your models here.
class PassModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], null=True, blank=True)
    pass_img = models.ImageField(upload_to='pass/', null=True, blank=True)
    qr = models.ImageField(upload_to='qr', null=True, blank=True)
    recognized = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} {self.email} {self.phone_number}"
    
    def save(self, *args, **kwargs):
        
        try:
            os.remove(self.qr.path)
        except:
            pass
            print("cannot remopved")
        
        str = f"{self.name},{self.email},{self.phone_number},{self.unique_id}"
        qr_image = qrcode.make(str)
        qr_offset = Image.new('RGB', (410, 410), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.name}_{self.email}_{self.phone_number}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, "PNG")

        self.qr.save(files_name, File(stream), save=False)
        qr_offset.close()
        super().save(*args, **kwargs)
       
  
  
def pass_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pass_pre_save_receiver, sender=PassModel)      