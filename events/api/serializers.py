from rest_framework import serializers
from ..models import Event
from fest.models import FestModel


class EventSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Event
        fields = ("event_name", "about")
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
        