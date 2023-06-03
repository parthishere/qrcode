from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class FestModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, null=True)
    banner = models.ImageField(upload_to='{user}/fest/', null=True, blank=True)
    about = models.TextField(null=True)
    removed = models.BooleanField(default=False)
    