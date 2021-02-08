from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.mailing import send_reset_password
from users.serializers import LoginSerializer, RegistrationSerializer, ChangePasswordSerializer, \
    ResetPasswordSerializer, UserSerializer
from configs.constants import BAD_REQUEST_MESSAGE


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)
        return Response(data=UserSerializer(user.applicant).data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data={"message": _("Registration was successful!")}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={"message": _("User with this email already exists.")},
                            status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, user=request.user)
        if serializer.is_valid():
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response(data={"message": _("Password changed successfully.")}, status=status.HTTP_200_OK)
        return Response(data={"message": BAD_REQUEST_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            send_reset_password(request.data['email'])
            return Response(data={"message": _("New password sent to email.")}, status=status.HTTP_200_OK)
        return Response(data={"message": _("We have a problems.")}, status=status.HTTP_400_BAD_REQUEST)
