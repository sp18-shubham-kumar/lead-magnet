from rest_framework.views import APIView
from rest_framework import status
from ...models import ReportItem
from ...serializers import ReportItemSerializer
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from django.shortcuts import get_object_or_404
from ...permissions import CustomIsAdminUser


class ReportItemListCreateView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request, report_history_id):
        items = ReportItem.objects.filter(report_id=report_history_id)
        serializer = ReportItemSerializer(items, many=True)
        return send_response(
            data=serializer.data,
            show_to_user=True,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    def post(self, request, report_history_id):
        data = request.data.copy()
        data["report"] = report_history_id
        serializer = ReportItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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


class ReportItemDetailView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request, report_history_id, pk):
        item = get_object_or_404(
            ReportItem, pk=pk, report_id=report_history_id)
        serializer = ReportItemSerializer(item)
        return send_response(
            data=serializer.data,
            show_to_user=True,
            message=ResponseMessages.DATA_FETCH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )

    def put(self, request, report_history_id, pk):
        item = get_object_or_404(
            ReportItem, pk=pk, report_id=report_history_id)
        data = request.data.copy()
        data["report"] = report_history_id
        serializer = ReportItemSerializer(item, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return send_response(
                data=serializer.data,
                show_to_user=True,
                message=ResponseMessages.DATA_UPDATE_SUCCESS,
                status_code=status.HTTP_200_OK,
            )
        return send_response(
            data=serializer.errors,
            show_to_user=True,
            level="error",
            message=ResponseMessages.INVALID_PAYLOAD,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, report_history_id, pk):
        item = get_object_or_404(
            ReportItem, pk=pk, report_id=report_history_id)
        item.delete()
        return send_response(
            data={"detail": ResponseMessages.RECORD_DELETED},
            show_to_user=True,
            message=ResponseMessages.RECORD_DELETED,
            status_code=status.HTTP_204_NO_CONTENT,
        )
