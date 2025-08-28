from rest_framework import serializers
from .models import Chakra, ChakraLog


class ChakraSerializer(serializers.ModelSerializer):
    # Serializer for the Chakra master data model (static definitions).

    class Meta:
        model = Chakra
        fields = [
            'id',
            'code',
            'name',
            'sanskrit_name',
            'color',
            'element',
            'description',
            'is_active',
        ]


class ChakraLogSerializer(serializers.ModelSerializer):
    # Serializer for user chakra logs, with nested chakra details for read.

    # Show chakra details (read-only nested representation)
    chakra_detail = ChakraSerializer(source='chakra', read_only=True)

    # Show username instead of user id
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ChakraLog
        fields = [
            'id',
            'user',
            'chakra',          
            'chakra_detail',    
            'state',
            'intensity',
            'notes',
            'solfeggio_frequency',
            'date',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_intensity(self, value):
        # Ensure intensity (if provided) is between 1 and 10.
        if value is not None and not (1 <= value <= 10):
            raise serializers.ValidationError("Intensity must be between 1 and 10.")
        return value
