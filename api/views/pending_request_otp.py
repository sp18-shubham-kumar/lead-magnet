from rest_framework.views import APIView
from rest_framework import status
from django.utils.crypto import get_random_string
from django.utils import timezone
from ..models import OTPVerification
from ..tasks import send_otp_email
from utils.restful_response import send_response


class PendingSendOTPView(APIView):
    """Send OTP specifically for pending requests"""

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return send_response(
                message="Email are required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        otp = get_random_string(length=6, allowed_chars="0123456789")
        OTPVerification.objects.create(email=email, otp_code=otp)

        send_otp_email.delay(email, otp)
        return send_response(
            message="Pending request OTP sent to your email",
            status_code=status.HTTP_200_OK
        )


class PendingVerifyOTPView(APIView):
    """Verify OTP for pending requests"""

    def post(self, request):
        email = request.data.get("email")
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
                return send_response(message="OTP already verified", status_code=status.HTTP_400_BAD_REQUEST)

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
                                     data={"attempts_left":remaining}, 
                                     status_code=status.HTTP_400_BAD_REQUEST)

        except OTPVerification.DoesNotExist:
            return send_response(
                message="Invalid OTP",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if otp_entry.is_expired():
            return send_response(
                message="OTP expired",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        otp_entry.is_verified = True
        otp_entry.verified_at = timezone.now()
        otp_entry.save()

        return send_response(
            message="Pending request OTP verified successfully",
            status_code=status.HTTP_200_OK
        )
