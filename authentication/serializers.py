import os

from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from authentication.models import Account, EmailConfirmationModel
from authentication.token import account_activation_token


class EmptySerializer(serializers.Serializer):
    pass


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'student_id', 'password')

    def validate(self, attrs):
        user = Account.objects.filter(email=attrs['email']).exists()

        if user:
            raise serializers.ValidationError({'email': 'User already exists with this email'})

        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be more than 6 characters."})

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        mail_subject = 'Activate your Todo Account'

        user = Account.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        EmailConfirmationModel.objects.create(
            uid=uidb64,
            token=token
        )

        email_body = os.getenv("CLIENT_URL") + 'email-verify?uid=' + uidb64 + '&token=' + token

        send_mail(mail_subject, email_body, settings.EMAIL_HOST_USER, [validated_data['email'], ])

        return user


class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationModel
        fields = '__all__'
