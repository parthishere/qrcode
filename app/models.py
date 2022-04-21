from django.db import models
from django.core.validators import MaxValueValidator
from io import BytesIO
import qrcode 
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.
class PassModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
    pass_img = models.ImageField(upload_to='pass/', null=True, blank=True)
    qr = models.ImageField(upload_to='qr', null=True, blank=True)
    recognized = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} {self.email} {self.phone_number}"
    
    def save(self, *args, **kwargs):
        str = f"{self.name},{self.email},{self.phone_number}"
        qr_image = qrcode.make(str)
        qr_offset = Image.new('RGB', (410, 410), 'white')
        qr_offset.paste(qr_image)
        files_name = f'{self.name}_{self.email}_{self.phone_number}qr.png'
        stream = BytesIO()
        qr_offset.save(stream, "PNG")
        if self.qr is None:
            self.qr.save(files_name, File(stream), save=False)
            qr_offset.close()
        else:
            pass
        super().save(*args, **kwargs)
        