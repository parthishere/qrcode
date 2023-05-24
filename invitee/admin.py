from django.contrib import admin

from .models import Invitee
# Register your models here.

class InviteesModelAdmin(admin.ModelAdmin):
    list_display = (
        "__str__", "id","email","unique_id", "recognized"
        )
    
admin.site.register(Invitee, InviteesModelAdmin)