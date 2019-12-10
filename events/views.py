# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events import constants
from events.models import Event, Choice, Room
from events.serializers import EventSerializer, ChoiceSerializer, \
    RoomSerializer, CreateBookSerializer


class EventView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class BookView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = RoomSerializer(Room.objects.all(), many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(applicant=request.user.applicant)
            return Response(data={'details': 'Successfully booked time.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SetChoiceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user.applicant)
            return Response(data={'details': 'User choice is set.'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class GetUncertainUsersByEventId(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         events = Event.objects.all()
#         data = []
#         for event in events:
#             q = Choice.objects.exclude(event__in=events)
#             data.append(q)
#
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         event_id = request.data.get('event_id')
#         event = get_object_or_404(Event, id=event_id)
#
#         data = []
#         if event:
#             for choice in Choice.objects.filter(event_id=event_id).filter(choice=constants.CONFUSED):
#                 data.append(ApplicantSerializer(choice.user).data)
#         return Response(data=data, status=status.HTTP_200_OK)

