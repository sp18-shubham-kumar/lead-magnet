from rest_framework import serializers
from ..models import ReportHistory, ReportItem


class ReportItemSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.role", read_only=True)
    role_level = serializers.CharField(source="role.level", read_only=True)
    role_exp_min = serializers.CharField(
        source="role.experience_min", read_only=True)
    role_exp_max = serializers.CharField(
        source="role.experience_max", read_only=True)

    from_location_name = serializers.SerializerMethodField()

    class Meta:
        model = ReportItem
        fields = [
            'id', 'report', 'role', 'role_name', 'role_level', 'role_exp_min', 'role_exp_max',
            'from_location', 'from_location_name', 'from_cost_usd',
            'sp18_cost_usd', 'savings_usd', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_from_location_name(self, obj):
        return f"{obj.from_location.country_name}"


class ReportHistorySerializer(serializers.ModelSerializer):
    items = ReportItemSerializer(many=True, read_only=True)
    lead_email = serializers.EmailField(source="lead.email", read_only=True)

    class Meta:
        model = ReportHistory
        fields = ['id', 'lead_email', 'report_file',
                  'status', 'sent_at', 'created_at', 'items']
        read_only_fields = ['id', 'created_at', 'status', 'sent_at', 'items']
