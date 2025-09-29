from rest_framework import serializers
from ..models import Location
from utils.location_handler import location_setter


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'country_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        country_name = data.get('country_name', getattr(
            instance, 'country_name', None))
        if not country_name:
            raise serializers.ValidationError(
                "Country Name is a required field.")

        data['country_name'] = location_setter(country_name)

        if country_name:
            existing_location = Location.objects.filter(
                country_name__iexact=country_name)
            if instance:
                existing_location = existing_location.exclude(id=instance.id)
            if existing_location.exists():
                raise serializers.ValidationError(
                    "A location with the same country name already exists.")
        return data
