from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from ...models import Role
from ...serializers import RoleSerializer
from ...permissions import CustomIsAdminUser
from rest_framework.renderers import JSONRenderer


class RoleListCreateView(APIView):
    """API for listing and creating roles"""
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        [CustomIsAdminUser()]

    def get(self, request):
        roles = Role.objects.all().order_by("id")
        serializer = RoleSerializer(roles, many=True)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=RoleSerializer)
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if not serializer.is_valid():
            return send_response(
                data=serializer.errors,
                show_to_user=True,
                level="error",
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return send_response(
            data=serializer.data,
            message=ResponseMessages.RECORD_CREATED,
            status_code=status.HTTP_201_CREATED,
        )


class RoleDetailView(APIView):
    """API for retrieve, update, delete"""
    renderer_classes = [JSONRenderer]

    def get_permissions(self):
        return [CustomIsAdminUser()]

    def get_object(self, pk):
        return get_object_or_404(Role, pk=pk)

    def get(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=RoleSerializer)
    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if not serializer.is_valid():
            return send_response(
                data=serializer.errors,
                show_to_user=True,
                level="error",
                message=ResponseMessages.INVALID_PAYLOAD,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        return send_response(
            data=serializer.data,
            message=ResponseMessages.DATA_UPDATE_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return send_response(
            data={},
            message=ResponseMessages.DATA_DELETED_SUCCESS,
            status_code=status.HTTP_204_NO_CONTENT,
        )
