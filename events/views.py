# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from events.models import Event, Book
from events.serializers import BookSerializer, EventSerializerPOST, EventSerializerGET


class EventView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventSerializerPOST
        else:
            return EventSerializerGET


class BookView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

