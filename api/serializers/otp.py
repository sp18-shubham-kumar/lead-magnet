from rest_framework import serializers
from ..models import OTPVerification


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPVerification
        fields = ["id", "email", "is_verified", "verified_at", "created_at"]
        read_only_fields = ['id', 'created_at', 'verified_at']
