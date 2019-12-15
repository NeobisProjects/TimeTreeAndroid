from django.utils.timezone import now
from rest_framework import serializers

from events import constants
from events.models import Book, Event, Choice, Room


class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date_begin', 'date_end', 'address',)


class BookSerializer(serializers.ModelSerializer):
    applicant = serializers.CharField(source='applicant.__str__')
    date_begin = serializers.DateField(source='get_date_begin')
    date_end = serializers.DateField(source='get_date_end')
    time_begin = serializers.TimeField(source='get_time_begin')
    time_end = serializers.TimeField(source='get_time_end')

    class Meta:
        model = Book
        fields = ('name', 'date_begin', 'time_begin',
                  'date_end', 'time_end',
                  'applicant',)


class RoomSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'location', 'books',)

    def get_books(self, room):
        q = Book.objects.filter(address=room, date_begin__gte=now())
        return BookSerializer(q, many=True).data


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('event', 'choice',)


class EventSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='get_date')
    time = serializers.TimeField(source='get_time')
    choice = serializers.IntegerField(source='get_choice')

    class Meta:
        model = Event
        fields = ('name', 'content', 'address',
                  'is_with_poll', 'deadline',
                  'date', 'time', 'choice')

    # def get_choice(self, event):
    #     choice = event.choices.filter(user=self.context['request'].user.applicant).first()
    #     return choice.choice if hasattr(choice, 'choice') else constants.CONFUSED


