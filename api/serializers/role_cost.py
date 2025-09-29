from rest_framework import serializers
from ..models import RoleCost


class RoleCostSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role', read_only=True)
    location_name = serializers.CharField(
        source='location.country_name', read_only=True)

    class Meta:
        model = RoleCost
        fields = ['id', 'role', 'location', 'cost_usd',
                  'created_at', 'updated_at', 'role_name', 'location_name']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        role = data.get('role', getattr(instance, 'role', None))
        location = data.get('location', getattr(instance, 'location', None))
        cost_usd = data.get('cost_usd', getattr(instance, 'cost_usd', None))

        if not role or not location or not cost_usd:
            raise serializers.ValidationError(
                "Role, Location, Cost in USD are required fields.")

        if cost_usd is not None and cost_usd < 0:
            raise serializers.ValidationError(
                "Cost in USD must be a non-negative value.")

        if role and location:
            existing_role_cost = RoleCost.objects.filter(
                role=role, location=location)
            if instance:
                existing_role_cost = existing_role_cost.exclude(id=instance.id)
            if existing_role_cost.exists():
                raise serializers.ValidationError(
                    "A role cost with the same role, location already exists.")

        return data
