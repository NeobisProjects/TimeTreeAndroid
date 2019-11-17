from rest_framework import serializers

from events.models import Book, Event, Choice, Room


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date', 'address',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date', 'applicant')


class RoomSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)

    class Meta:
        model = Room
        fields = ('id', 'name', 'location', 'books',)


class EventSerializer(serializers.ModelSerializer):
    # participants = serializers.PrimaryKeyRelatedField(many=True, queryset=Applicant.objects.all())

    class Meta:
        model = Event
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('event', 'choice',)
