from rest_framework import serializers
from ..models import Role


class RoleSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ['id', 'role', 'level', 'experience_min',
                  'experience_max', 'created_at', 'updated_at', 'display_name']
        read_only_fields = ['id', 'created_at', 'updated_at']
        ordering = ['created_at', 'updated_at']

    def get_display_name(self, obj):
        return f"{obj.role} ({obj.level}, {obj.experience_min}-{obj.experience_max} yrs)"

    def validate(self, data):
        instance = getattr(self, 'instance', None)

        role = data.get('role', getattr(instance, 'role', None))
        level = data.get('level', getattr(instance, 'level', None))
        experience_min = data.get('experience_min', getattr(
            instance, 'experience_min', None))
        experience_max = data.get('experience_max', getattr(
            instance, 'experience_max', None))

        if not role or not level:
            raise serializers.ValidationError(
                "Role and Level are required fields.")

        role = role.strip().title()
        data['role'] = role

        level = level.strip().title()
        data['level'] = level

        if experience_min is not None and experience_max is not None:
            if experience_min < 0 or experience_max < 0:
                raise serializers.ValidationError(
                    "Experience values must be non-negative.")
            if experience_min > experience_max:
                raise serializers.ValidationError(
                    "Minimum experience cannot be greater than maximum experience.")

        if role and level and experience_min is not None and experience_max is not None:
            existing_role = Role.objects.filter(
                role__iexact=role, level__iexact=level, experience_min=experience_min, experience_max=experience_max)
            if instance:
                existing_role = existing_role.exclude(id=instance.id)
            if existing_role.exists():
                raise serializers.ValidationError(
                    "A role with the same role, level, and experience range already exists.")
        return data
