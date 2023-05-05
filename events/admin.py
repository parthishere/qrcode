from django.contrib import admin

from .models import Event
# Register your models here.

class EventAdminModel(admin.ModelAdmin):
    list_display = (
        "__str__", "id", "created_by"
    )
    
admin.site.register(Event, EventAdminModel)