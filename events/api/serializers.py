from rest_framework import serializers
from ..models import Event
from fest.models import FestModel


class EventSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Event
        exclude = ("qr_code_coordinate_x","qr_code_coordinate_y", 'name_coordinate_x', "name_coordinate_y", "pre_define_pass")
        
        read_only_fields = ("unique_id", "organization_or_college", "created_by", 'moderators', "contact_number", "contact_email", "contact_number_2", "contact_email_2", "instance_created_date", 'updated_date', "online_events", "offline_events", "invitees", "recognized_invitees", "fast_check", "pass_template", "event_update_count", "removed", 'predefined_pass_image')
        # depth = 1
        
class EventDetailSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Event
        fields = ("__all__")
        # depth = 1

class EventUpdateFestPk(serializers.ModelSerializer):
    class Meta():
        model = Event
        fields = ("fest",)
    

class FestListSerializer(serializers.ModelSerializer):
    count_event = serializers.IntegerField()
    class Meta():
        model = FestModel
        fields = ("fest",)
        
    def get_count_event(self, obj):
        count = obj.events.count()
        return count 
        