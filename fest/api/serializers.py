from fest.models import FestModel
from rest_framework import serializers

class FestSerializer(serializers.ModelSerilaizers):
    class Meta():
        model = FestModel
        exclude = ("removed", "slug")
        read_only_fields = ("user")