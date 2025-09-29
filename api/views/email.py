from rest_framework.views import APIView
from rest_framework import status
from django.utils.crypto import get_random_string
from ..models import Lead, OTPVerification, ReportHistory
from ..tasks import send_otp_email, send_report_email
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.utils import timezone
from datetime import timedelta


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        company = request.data.get("company")

        if not email or not name:
            return send_response(message="Name and Email required", 
                                 status_code=status.HTTP_400_BAD_REQUEST)

        otp = get_random_string(length=6, allowed_chars="0123456789")
        OTPVerification.objects.create(email=email, otp_code=otp)

        send_otp_email.delay(email, otp)
        return send_response(message="OTP sent to your email", 
                             status_code=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        name = (request.data.get("name", "")).strip()
        company = (request.data.get("company", "")).strip()
        otp_code = request.data.get("otp_code")

        if not email or not otp_code:
            return send_response(
                message="Email and OTP code required",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            otp_entry = OTPVerification.objects.filter(
                email=email).latest("created_at")
            if otp_entry.is_verified:
                return send_response(message="OTP already verified", 
                                     status_code=status.HTTP_400_BAD_REQUEST)

            if otp_entry.attempts >= 2:
                return send_response(
                    message="Maximum attempts reached. Please request a new OTP.",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            if otp_entry.otp_code != otp_code:
                otp_entry.attempts += 1
                otp_entry.save()
                remaining = 3 - otp_entry.attempts
                return send_response(message=f"Invalid OTP. {remaining} attempts left.", 
                                     data={"attempts_left": remaining}, 
                                     status_code=status.HTTP_400_BAD_REQUEST)

        except OTPVerification.DoesNotExist:
            return send_response(message="Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST)

        if otp_entry.is_expired():
            return send_response(message="OTP expired", status_code=status.HTTP_400_BAD_REQUEST)

        otp_entry.is_verified = True
        otp_entry.verified_at = timezone.now()
        otp_entry.save()
        lead, created = Lead.objects.get_or_create(email=email)

        updated = False

        if name and (not lead.name or lead.name.strip() != name.strip()):
            lead.name = name.strip()
            updated = True

        if company and (not lead.company or lead.company.strip() != company.strip()):
            lead.company = company.strip()
            updated = True

        if updated:
            lead.save()

        return send_response(message="OTP verified successfully", status_code=status.HTTP_200_OK)


class SendReportView(APIView):
    def post(self, request):
        email = request.data.get("email")
        report_id = request.data.get("report_id")
        if not email or not report_id:
            return send_response(message="Email and Report ID required", status_code=status.HTTP_400_BAD_REQUEST)

        otp = OTPVerification.objects.filter(email=email).latest("created_at")
        if not otp.is_verified:
            return send_response(message="OTP not verified", status_code=status.HTTP_403_FORBIDDEN)

        if otp.verified_at < timezone.now() - timedelta(minutes=ResponseMessages.VALIDITY_MINUTES):
            return send_response(message=ResponseMessages.REQUEST_FAILED_OR_OTP_EXPIRED, 
                                 status_code=status.HTTP_403_FORBIDDEN)

        try:
            report = ReportHistory.objects.get(id=report_id, lead__email=email)
        except ReportHistory.DoesNotExist:
            return send_response(message=ResponseMessages.NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)

        if report.status == "generated":
            if report.created_at < otp.verified_at:
                return send_response(message="you can only send the report generated after your last OTP verification", 
                                     status_code=status.HTTP_403_FORBIDDEN)
            send_report_email.delay(email, report_id)
            return send_response(message="Your hiring cost report will be sent shortly.",
                                 status_code=status.HTTP_200_OK)

        elif report.status == "sent":
            send_report_email.delay(email, report_id)
            return send_response(message="Your hiring cost report will be sent shortly.",
                                 status_code=status.HTTP_200_OK)

        else:
            return send_response(message=f"Cannot send report with status {report.status}", 
                                 status_code=status.HTTP_400_BAD_REQUEST)
