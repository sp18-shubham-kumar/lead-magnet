from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import AdminLoginSerializer
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from drf_yasg.utils import swagger_auto_schema


User = get_user_model()


class AdminLoginView(APIView):
    template_name = "admin/login.html"

    def get(self, request):
        return render(request, self.template_name)

    @swagger_auto_schema(request_body=AdminLoginSerializer)
    def post(self, request):
        data = request.data if request.content_type == 'application/json' else request.POST
        serializer = AdminLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email, password=password)

        if user is None:
            if request.content_type != "application/json":
                return render(request, self.template_name, {'error': ResponseMessages.INVALID_CREDENTIALS})
            return send_response(
                data={"detail": ResponseMessages.EMAIL_PASSWORD_INCORRECT},
                show_to_user=True,
                level="error",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_superuser:
            if request.content_type != "application/json":
                return render(request, self.template_name, {'error': ResponseMessages.NOT_AUTHORIZED})
            return send_response(
                data={"detail": ResponseMessages.NOT_AUTHORIZED},
                show_to_user=True,
                level="error",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        auth_login(request, user)

        if request.content_type != "application/json":
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            return redirect('admin-dashboard')

        return send_response(
            data={
                "refresh": str(refresh),
                "access": str(access_token),
            },
            show_to_user=True,
            message=ResponseMessages.AUTH_SUCCESS,
            status_code=status.HTTP_200_OK,
        )
