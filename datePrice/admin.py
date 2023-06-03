from django.contrib import admin

# Register your models here.
from .models import DatePrice, OfflineModel, VirtualModel

admin.site.register(VirtualModel)
admin.site.register(OfflineModel)
admin.site.register(DatePrice)