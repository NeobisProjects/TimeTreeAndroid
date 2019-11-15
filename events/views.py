# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applicants.models import Applicant
from applicants.serializers import ApplicantSerializer
from events import constants
from events.models import Event, Choice
from events.serializers import BookSerializer, EventSerializerPOST, EventSerializerGET, ChoiceSerializer


class EventView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventSerializerPOST
        else:
            return EventSerializerGET


class BookView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pass

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(applicant=request.user.applicant)
            return Response(data={'details': 'Successfully book time.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SetChoiceView(APIView):
    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user.applicant)
            return Response(data={'details': 'User choice is set.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetUncertainUsers(APIView):
    def post(self, request):
        print(Choice.objects.all())
        event_id = request.data.get('event_id')
        event = get_object_or_404(Event, id=event_id)

        data = []
        if event:
            for choice in Choice.objects.filter(event_id=event_id).filter(user=request.user.applicant):
                serializer = ApplicantSerializer(Applicant.objects.filter(email=choice.user.email)).data
                data.append(serializer)
        return Response(data=data, status=status.HTTP_200_OK)
