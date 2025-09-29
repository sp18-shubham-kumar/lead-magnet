from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from rest_framework import status
from ..models import ReportHistory, Lead, OTPVerification
from ..serializers import ReportHistorySerializer
from django.utils import timezone
from datetime import timedelta


class PrevReportsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return send_response(status_code=status.HTTP_400_BAD_REQUEST)
        last_verification = (
            OTPVerification.objects.filter(email=email)
            .latest("created_at")
        )

        if not last_verification.is_verified:
            return send_response(message="OTP not verified", 
                                 status_code=status.HTTP_403_FORBIDDEN)

        if last_verification.verified_at < timezone.now() - timedelta(minutes=ResponseMessages.VALIDITY_MINUTES):
            return send_response(message=ResponseMessages.REQUEST_FAILED_OR_OTP_EXPIRED, 
                                 status_code=status.HTTP_403_FORBIDDEN)

        try:
            lead = Lead.objects.get(email=email)
        except Lead.DoesNotExist:
            return send_response(message=ResponseMessages.NOT_FOUND, 
                                 status_code=status.HTTP_404_NOT_FOUND)

        reports = ReportHistory.objects.filter(
            lead=lead, status="sent").order_by("created_at")
        serializer = ReportHistorySerializer(reports, many=True)
        return send_response(data=serializer.data, status_code=status.HTTP_200_OK)
