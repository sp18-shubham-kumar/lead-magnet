from rest_framework.views import APIView
from rest_framework import status
from ..models import Location, Role
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class AvailableRolesView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'from_location', openapi.IN_QUERY,
                description="ID of source location (country)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ]
    )
    def get(self, request):
        from_location_id = request.query_params.get('from_location')

        if not from_location_id:
            return send_response(
                data={"detail": "from_location is required."},
                show_to_user=True,
                level="error",
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Get SP18 location  
        # (make sure you have one entry in Location table for Spark Eighteen)
        sp18 = get_object_or_404(
            Location, country_name__iexact="Spark Eighteen")

        roles = Role.objects.filter(
            rolecosts__location_id=from_location_id
        ).filter(
            rolecosts__location=sp18
        ).distinct()

        data = [
            {
                "id": r.pk,
                "name": r.role,
                "level": r.level,
                "experience_min": r.experience_min,
                "experience_max": r.experience_max,
            }
            for r in roles
        ]

        return send_response(
            data=data,
            show_to_user=True,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )
