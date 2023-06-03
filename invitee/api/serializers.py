from invitee.models import Invitee
from rest_framework import serializers

class InviteeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Invitee
        fields = ("__all__")
        depth =1
        
class BulkCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    event_id = serializers.IntegerField()