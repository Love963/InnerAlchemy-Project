from rest_framework import serializers
from .models import SoulNote


class SoulNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoulNote
        fields = '__all__'