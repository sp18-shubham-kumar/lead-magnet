from ...models import OTPVerification
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from ...permissions import CustomIsAdminUser
from rest_framework import status
from rest_framework.views import APIView
from ...serializers import OTPSerializer


class OTPlistView(APIView):
    permission_classes = [CustomIsAdminUser]

    def get(self, request):
        otps = OTPVerification.objects.all()
        serializer = OTPSerializer(otps, many=True)
        return send_response(data=serializer.data, 
                             message=ResponseMessages.DATA_FETCH_SUCCESS, 
                             status_code=status.HTTP_200_OK)
