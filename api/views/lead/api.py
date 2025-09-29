from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ...serializers import LeadSerializer
from ...models import Lead
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from ...permissions import CustomIsAdminUser


# ---------- API VIEWS ---------- #
class LeadListCreateView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request):
        leads = Lead.objects.all()
        serializer = LeadSerializer(leads, many=True)
        return send_response(data=serializer.data, 
                             message=ResponseMessages.DATA_FETCH_SUCCESS, 
                             status_code=status.HTTP_200_OK)

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            lead = serializer.save()
            return send_response(
                data=LeadSerializer(lead).data,
                message="Lead Created",
                status_code=status.HTTP_201_CREATED
            )
        return send_response(
            data=serializer.errors,
            show_to_user=True,
            level="error",
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class LeadDetailView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead)
        return send_response(data=serializer.data, 
                             message=ResponseMessages.DATA_FETCH_SUCCESS, 
                             status_code=status.HTTP_200_OK)

    def put(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            lead = serializer.save()
            return send_response(
                data=LeadSerializer(lead).data,
                message=ResponseMessages.DATA_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK
            )
        return send_response(
            data=serializer.errors,
            show_to_user=True,
            level="error",
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk)
        lead.delete()
        return send_response(message=ResponseMessages.RECORD_DELETED, 
                             status_code=status.HTTP_204_NO_CONTENT)
