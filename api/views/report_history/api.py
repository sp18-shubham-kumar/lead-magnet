from rest_framework.views import APIView
from rest_framework import status
from ...models import ReportHistory
from ...serializers import ReportHistorySerializer
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.shortcuts import get_object_or_404
from ...permissions import CustomIsAdminUser


class ReportHistoryListCreateView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request):
        reports = ReportHistory.objects.all()
        serializer = ReportHistorySerializer(reports, many=True)
        return send_response(
            data=serializer.data,
            show_to_user=True,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ReportHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(status="generated")
            return send_response(
                data=serializer.data,
                show_to_user=True,
                message=ResponseMessages.RECORD_CREATED,
                status_code=status.HTTP_201_CREATED,
            )
        return send_response(
            data=serializer.errors,
            show_to_user=True,
            level="error",
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class ReportHistoryDetailView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request, pk):
        report = get_object_or_404(ReportHistory, pk=pk)
        serializer = ReportHistorySerializer(report)
        return send_response(
            data=serializer.data,
            show_to_user=True,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        report = get_object_or_404(ReportHistory, pk=pk)
        report.delete()
        return send_response(
            data={"detail": ResponseMessages.RECORD_DELETED},
            show_to_user=True,
            message=ResponseMessages.RECORD_DELETED,
            status_code=status.HTTP_204_NO_CONTENT,
        )
