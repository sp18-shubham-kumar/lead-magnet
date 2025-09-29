from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from ...models import Location
from ...serializers import LocationSerializer
from ...permissions import CustomIsAdminUser
# ---------------------- API VIEWS ---------------------- #


class LocationListCreateView(APIView):
    """API for listing and creating locations"""

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [CustomIsAdminUser()]

    def get(self, request):
        if not request.user.is_staff:
            locations = Location.objects.exclude(
                country_name__iexact="Spark Eighteen").order_by("id")
        else:
            locations = Location.objects.all().order_by("id")

        serializer = LocationSerializer(locations, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=LocationSerializer)
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if not serializer.is_valid():
            return send_response(
                data=serializer.errors,
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return send_response(
            data=serializer.data,
            message=ResponseMessages.RECORD_CREATED,
            status_code=status.HTTP_201_CREATED
        )


class LocationDetailView(APIView):
    """API for retrieve, update, delete"""

    def get_permissions(self):
        [CustomIsAdminUser()]

    def get_object(self, pk):
        return get_object_or_404(Location, pk=pk)

    def get(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=LocationSerializer)
    def put(self, request, pk):
        location = self.get_object(pk)
        serializer = LocationSerializer(
            location, data=request.data, partial=True)
        if not serializer.is_valid():
            return send_response(
                data=serializer.errors,
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_UPDATE_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        location = self.get_object(pk)
        location.delete()
        return send_response(
            data={},
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT
        )
