from rest_framework import serializers
from .models import VisualizationAffirmation


class VisualizationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")  # only show username
    solfeggio_frequency = serializers.StringRelatedField(read_only=True) 
    solfeggio_frequency_id = serializers.PrimaryKeyRelatedField(
        source="solfeggio_frequency",
        queryset=VisualizationAffirmation._meta.get_field("solfeggio_frequency").remote_field.model.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = VisualizationAffirmation
        fields = [
            "id",
            "user",
            "title",
            "content",
            "tags",
            "solfeggio_frequency",
            "solfeggio_frequency_id", 
            "date_created",
            "updated_at",  
        ]
        read_only_fields = ["id", "user", "date_created", "updated_at"]
