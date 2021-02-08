from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from configs.constants import BAD_REQUEST_MESSAGE
from events.models import Event, Room
from events.serializers import EventSerializer, ChoiceSerializer, \
    RoomSerializer, CreateBookSerializer, CreateRoomSerializer


class EventView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(choices__user=self.request.user,
                                    date__gte=timezone.now()) | \
               Event.objects.filter(is_with_poll=False, date__gte=timezone.now())


class EventWithPollView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
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
            return Response(data={'message': _('Successfully booked time.')}, status=status.HTTP_201_CREATED)
        return Response(data={'message': BAD_REQUEST_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)


class SetChoiceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'message': _('User choice is set.')}, status=status.HTTP_201_CREATED)


class RoomsView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
