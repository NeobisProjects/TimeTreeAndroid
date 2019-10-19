from django.contrib.auth import authenticate
from rest_framework import serializers

from applicants.models import Applicant


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('department', 'university',
                  'name', 'surname', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True,
                                     style={'input_type': 'password',
                                            'placeholder': 'Password',
                                            })

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('An username is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')
        return data
