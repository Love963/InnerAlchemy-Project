from rest_framework import serializers
from .models import Chakra, ChakraLog

class ChakraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chakra
        fields = ['id', 'code', 'name', 'sanskrit_name', 'color', 'element', 'description', 'is_active']
class ChakraLogSerializer(serializers.ModelSerializer):
    # Show nested chakra read_only summary; accept chakra id on write
    chakra_detail = ChakraSerializer(source='chakra', read_only=True)

    class Meta:
        model = ChakraLog
        fields = [
            'id', 'user', 'chakra', 'chakra_detail', 'state', 'intensity',
            'notes', 'solfeggio_frequency', 'date', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

        def validate_intensity(self, value):
            if value is not None and not (1 <= value <= 10):
                raise serializers.ValidationError('Intensity must be between 1 and 10.')
            return value