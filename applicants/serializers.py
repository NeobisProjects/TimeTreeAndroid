from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

from applicants.mailing import send_greeting_mail
from applicants.models import Applicant


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Applicant
        fields = ('name', 'surname', 'email', 'password', 'password2', 'department')

    def create(self, validate_data):
        password = validate_data.pop('password')
        instance = super(RegistrationSerializer, self).create(validate_data)
        user = User.objects.get(username=instance.email)
        user.set_password(password)
        user.save()
        send_greeting_mail(instance.email)
        return instance

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password and password2:
            if password != password2:
                raise serializers.ValidationError('Passwords must me equal!')

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True,
                                     style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email is required to log in.')
        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100, write_only=True,
                                         style={'input_type': 'password'})
    new_password = serializers.CharField(max_length=100, write_only=True,
                                         style={'input_type': 'password'})
    new_password_check = serializers.CharField(max_length=100, write_only=True,
                                               style={'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        user = self.user
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)
        new_password_check = data.get('new_password_check', None)

        if old_password is None:
            raise serializers.ValidationError('An old password is required to change password.')
        if new_password is None:
            raise serializers.ValidationError('A new password is required.')
        if new_password_check is None:
            raise serializers.ValidationError('Please confirm new password')
        if new_password != new_password_check:
            raise serializers.ValidationError('Passwords must be similar.')

        user = authenticate(username=user.username, password=old_password)
        if user is None:
            raise serializers.ValidationError('You input incorrect password. Please try again!')

        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate(self, attrs):
        email = attrs.get('email', None)
        if email is None:
            raise serializers.ValidationError('Email address is required.')

        user = User.objects.get(username=email)
        if not user:
            raise serializers.ValidationError('There is no user with this email.')

        return attrs
