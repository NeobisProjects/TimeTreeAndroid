# Create your views here.
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from configs.constants import BAD_REQUEST_MESSAGE
from events.models import Event, Room
from events.serializers import EventSerializer, ChoiceSerializer, \
    RoomSerializer, CreateBookSerializer


class EventView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(choices__user=self.request.user, date__gte=timezone.now())


class EventWithPollView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # queryset = Event.objects.filter(is_with_poll__isnull=True)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(choices__user=self.request.user,
                                    date__gte=timezone.now(),
                                    is_with_poll=True)


class BookView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = RoomSerializer(Room.objects.all(), many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(applicant=request.user)
            return Response(data={'message': 'Successfully booked time.'}, status=status.HTTP_201_CREATED)
        return Response(data={'message': BAD_REQUEST_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)


class SetChoiceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response(data={'message': 'User choice is set.'}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(data={'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'message': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
