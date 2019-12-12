from django.utils.timezone import now
from rest_framework import serializers

from events.models import Book, Event, Choice, Room


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date', 'address',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date', 'applicant',)


class RoomSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'location', 'books',)

    def get_books(self, room):
        print(room)
        q = Book.objects.filter(address=room, date__gte=now())
        return BookSerializer(q, many=True).data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('event', 'choice',)
