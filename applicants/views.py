from django.contrib.auth import authenticate, login
# Create your views here.
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applicants.mailing import send_reset_password
from applicants.models import Applicant
from applicants.serializers import LoginSerializer, RegistrationSerializer, ChangePasswordSerializer, \
    ResetPasswordSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            if not hasattr(user, 'applicant'):
                applicant_id = 'admin'
            else:
                applicant_id = user.applicant.pk

            data = {
                'token': token.key,
                'applicant_id': applicant_id,
                'email': user.email
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = Applicant.objects.all()


class ChangePasswordAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response(data={"details": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(data={"details": "We have a problems."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_reset_password(request.data['email'])
            return Response(data={"details": "New password send to email."}, status=status.HTTP_200_OK)
        return Response(data={"details": "We have a problems."}, status=status.HTTP_400_BAD_REQUEST)
