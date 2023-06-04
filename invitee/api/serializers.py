from invitee.models import Invitee
from rest_framework import serializers

class InviteeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Invitee
        fields = ("__all__")
        read_only_fields = ("user", "event", "created_by", "created_on", "unique_id", "updated_on", "recognized", "qr_code", "pass_template", 'sent_email')
        
class BulkCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    event_id = serializers.IntegerField()