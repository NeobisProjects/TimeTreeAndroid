from django.contrib.auth import authenticate, login
# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applicants.mailing import send_greeting_mail
from applicants.serializers import LoginSerializer, RegistrationSerializer, ChangePasswordSerializer


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


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            applicant = serializer.save()
            send_greeting_mail(applicant.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data['email'] = request.user.username
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
