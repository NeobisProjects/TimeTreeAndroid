from rest_framework import serializers

from applicants.models import Applicant
from applicants.serializers import RegistrationSerializer
from events.models import Book, Event, Choice


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'date', 'address',)


class EventSerializerPOST(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=Applicant.objects.all())

    class Meta:
        model = Event
        fields = '__all__'


class EventSerializerGET(serializers.ModelSerializer):
    participants = RegistrationSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('event', 'choice',)
