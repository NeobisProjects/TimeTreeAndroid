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

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            if not hasattr(user, 'applicant'):
                data = {
                    'is_staff': user.is_staff,
                    'token': token.key,
                    'applicant_id': -1,
                    'email': user.email,
                    'name': None,
                    'surname': None,
                    'department': None,
                }
            else:
                data = {
                    'is_staff': user.is_staff,
                    'token': token.key,
                    'applicant_id': user.applicant.pk,
                    'email': user.email,
                    'name': user.applicant.name,
                    'surname': user.applicant.surname,
                    'department': user.applicant.department_id,
                }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": BAD_REQUEST_MESSAGE}, status=status.HTTP_404_NOT_FOUND)


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = Applicant.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data={"message": "Registration was successful!"}, status=status.HTTP_201_CREATED)
        return Response(data={"message": BAD_REQUEST_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, user=request.user)
        if serializer.is_valid(raise_exception=True):
            request.user.set_password(request.data['new_password'])
            request.user.save()
            return Response(data={"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(data={"message": BAD_REQUEST_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_reset_password(request.data['email'])
            return Response(data={"message": "New password send to email."}, status=status.HTTP_200_OK)
        return Response(data={"message": "We have a problems."}, status=status.HTTP_400_BAD_REQUEST)
