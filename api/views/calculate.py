from rest_framework.views import APIView
from rest_framework import status
from ..models import (ReportHistory, ReportItem, Location, 
                      Role, RoleCost, Lead, OTPVerification)
from ..serializers import ReportItemSerializer
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta


class CalculateReportView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['from_location', 'roles', 'lead_email'],
            properties={
                'from_location': openapi.Schema(type=openapi.TYPE_INTEGER, 
                                                description="Source location ID"),
                'roles': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description="List of role IDs"
                ),
                'lead_email': openapi.Schema(type=openapi.TYPE_STRING, 
                                             description="Lead Email"),
            },
            example={
                "from_location": 1,
                "roles": [1, 2, 3],
                "lead_email": "test@example.com"
            }
        ),
        responses={
            201: openapi.Response(
                description="Report created successfully"
            ),
            400: "Invalid payload"
        }
    )
    def post(self, request):
        from_location_id = request.data.get('from_location')
        role_ids = request.data.get('roles', [])
        lead_email = request.data.get('lead_email')

        if not from_location_id or not role_ids or not lead_email:
            return send_response(
                data={"detail": "from_location, roles and lead email are required."},
                show_to_user=True,
                level="error",
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        from_location = get_object_or_404(Location, pk=from_location_id)
        sp18 = get_object_or_404(
            Location, country_name__iexact="Spark Eighteen")
        lead = get_object_or_404(Lead, email=lead_email)

        last_verification = (
            OTPVerification.objects.filter(email=lead_email)
            .latest("created_at")
        )

        if not last_verification.is_verified:
            return send_response(message="OTP not verified", status_code=status.HTTP_403_FORBIDDEN)

        if last_verification.verified_at < timezone.now() - timedelta(minutes=ResponseMessages.VALIDITY_MINUTES):
            return send_response(message=ResponseMessages.REQUEST_FAILED_OR_OTP_EXPIRED, 
                                 status_code=status.HTTP_403_FORBIDDEN)

        report = ReportHistory.objects.create(lead=lead, status="generated")
        items = []
        total_usd = 0

        for role_id in role_ids:
            role = get_object_or_404(Role, pk=role_id)

            try:
                rc_from = RoleCost.objects.get(
                    role=role, location=from_location)
                rc_sp18 = RoleCost.objects.get(role=role, location=sp18)
            except RoleCost.DoesNotExist:
                continue

            savings_usd = rc_from.cost_usd - rc_sp18.cost_usd
            total_usd += savings_usd

            item = ReportItem.objects.create(
                report=report,
                role=role,
                from_location=from_location,
                sp18_cost_usd=rc_sp18.cost_usd,
                from_cost_usd=rc_from.cost_usd,
                savings_usd=savings_usd,
            )
            items.append(item)

        return send_response(
            data={
                "report_id": report.pk,
                "status": report.status,
                "items": ReportItemSerializer(items, many=True).data,
                "total_savings_usd": total_usd
            },
            show_to_user=True,
            message=ResponseMessages.RECORD_CREATED,
            status_code=status.HTTP_201_CREATED
        )
