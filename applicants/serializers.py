from django.contrib.auth import authenticate
from rest_framework import serializers

from applicants.mailing import send_greeting_mail
from applicants.models import Applicant


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('name', 'surname', 'email', 'department', 'university',)

    def create(self, validate_data):
        instance = super(RegistrationSerializer, self).create(validate_data)
        send_greeting_mail(instance.email)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True,
                                     style={'input_type': 'password',
                                            'placeholder': 'Password',
                                            })

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
    old_password = serializers.CharField(max_length=50, write_only=True,
                                         style={'input_type': 'password',
                                                'placeholder': 'Password',
                                                })
    new_password = serializers.CharField(max_length=50, write_only=True,
                                         style={'input_type': 'password',
                                                'placeholder': 'Password',
                                                })
    new_password_check = serializers.CharField(max_length=50, write_only=True,
                                               style={'input_type': 'password',
                                                      'placeholder': 'Password',
                                                      })
    email = serializers.EmailField()

    def validate(self, request):
        old_password = request.get('old_password', None)
        new_password = request.get('new_password', None)
        new_password_check = request.get('new_password_check', None)
        email = request.get('email', None)
        if old_password is None:
            raise serializers.ValidationError('An old password is required to change password.')

        if new_password is None:
            raise serializers.ValidationError('A new password is required.')

        if new_password_check is None:
            raise serializers.ValidationError('Please confirm new password')

        if new_password != new_password_check:
            raise serializers.ValidationError('Passwords must be similar.')

        user = authenticate(username=email, password=old_password)

        if user is None:
            raise serializers.ValidationError('You input incorrect password. Please try again!')

        user.set_password(new_password)
        user.save()

        return request


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('id', 'name', 'surname',)
