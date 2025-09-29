from rest_framework.views import APIView
from utils.data_constants import ResponseMessages
from utils.restful_response import send_response
from rest_framework import status
from ...models import OTPVerification, PendingRequest
from ...tasks import notify_admin_pending_request


class PendingRequestListCreateView(APIView):
    """Save a pending request after OTP verification"""

    def get(self, request):
        # --- admin can view all requests ---
        if not request.user.is_authenticated or not request.user.is_staff:
            return send_response(
                message=ResponseMessages.NOT_AUTHORIZED,
                status_code=status.HTTP_403_FORBIDDEN
            )

        pending_requests = PendingRequest.objects.all().order_by("-created_at")
        data = [
            {
                "id": pr.id,
                "name": pr.name,
                "email": pr.email,
                "company": pr.company,
                "location": pr.location,
                "roles": pr.roles,
                "created_at": pr.created_at,
            }
            for pr in pending_requests
        ]
        return send_response(
            message="Pending requests fetched successfully",
            data=data,
            status_code=status.HTTP_200_OK
        )

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name")
        company = request.data.get("company")
        location = request.data.get("location")
        roles = request.data.get("roles")

        if not all([email, name, location, roles]):
            return send_response(
                message="Name, Email, Location, and Roles are required",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # check OTP verified
        otp_entry = OTPVerification.objects.filter(
            email=email).latest("created_at")
        if not otp_entry.is_verified:
            return send_response(
                message="Please verify OTP first",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        pending = PendingRequest.objects.create(
            name=name,
            email=email,
            company=company,
            location=location,
            roles=roles,
        )
        notify_admin_pending_request.delay(pending.id)

        return send_response(
            message="Your request has been submitted successfully",
            data={"id": pending.id},
            status_code=status.HTTP_201_CREATED
        )
