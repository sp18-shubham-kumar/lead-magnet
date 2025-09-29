from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages

from ...models import RoleCost
from ...serializers import RoleCostSerializer
from ...permissions import CustomIsAdminUser


class RoleCostListCreateView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request):
        rolecosts = RoleCost.objects.all().select_related(
            'role', 'location').order_by('id')
        serializer = RoleCostSerializer(rolecosts, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=RoleCostSerializer)
    def post(self, request):
        serializer = RoleCostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.RECORD_CREATED,
                status_code=status.HTTP_201_CREATED
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class RoleCostDetailView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(RoleCost, pk=pk)

    def get(self, request, pk):
        rolecost = self.get_object(pk)
        serializer = RoleCostSerializer(rolecost)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK
        )

    @swagger_auto_schema(request_body=RoleCostSerializer)
    def put(self, request, pk):
        rolecost = self.get_object(pk)
        serializer = RoleCostSerializer(
            rolecost, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK
            )
        return send_response(
            data=serializer.errors,
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        rolecost = self.get_object(pk)
        rolecost.delete()
        return send_response(
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT
        )
