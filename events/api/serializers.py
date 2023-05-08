from rest_framework import serializers
from ..models import Event
from accounts.models import Invitee

class EventSerializer(serializers.ModelSerializer):
    class Meta():
        model = Event
        fields = ("__all__")
        # depth = 1
        
class InviteeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Invitee
        fields = ("__all__")
        depth =1
        
class BulkCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    event_id = serializers.IntegerField()
    