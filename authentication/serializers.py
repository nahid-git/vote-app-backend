import smtplib

from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.response import Response

from authentication.models import Account, EmailConfirmationModel, ForgotPasswordModel
from authentication.token import account_activation_token
from authentication.utils import sent_user_verify_email, sent_reset_password_email


class EmptySerializer(serializers.Serializer):
    pass


class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = Account
        fields = ['email', 'student_id', 'password', 'confirm_password']

    def validate(self, attrs):
        user = Account.objects.filter(email=attrs['email']).exists()

        if user:
            raise serializers.ValidationError({'email': 'User already exists with this email'})

        student_id = Account.objects.filter(student_id=attrs['student_id']).exists()

        if student_id:
            raise serializers.ValidationError({'student_id': 'Student already exists with this ID'})

        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be more than 8 characters."})

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = Account.objects.create(
            email=validated_data['email'],
            is_active=False
        )
        user.student_id = validated_data['student_id']
        user.set_password(validated_data['password'])
        user.save()
        try:
            sent_user_verify_email(user)
        except smtplib.SMTPException as e:
            user.delete()
            return Response({'message': 'Internal Server Error.'})
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        try:
            user = Account.objects.get(email=attrs['email'], is_active=True)
            if not user.check_password(attrs['password']):
                raise serializers.ValidationError({'password': 'Email or password is incorrect'})
        except Exception:
            raise serializers.ValidationError({"password": "Email or password is incorrect"})
        return attrs


class EmailConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationModel
        fields = '__all__'


class EmailVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailConfirmationModel
        fields = ['uid', 'token']

    def validate(self, attrs):
        if attrs['uid'] is not None and attrs['token'] is not None:
            email_user = EmailConfirmationModel.objects.filter(uid=attrs['uid'], token=attrs['token']).exists()

            if not email_user:
                raise serializers.ValidationError({'non_field_errors': ['Token or uid is invalid!']})

            uid = force_str(urlsafe_base64_decode(attrs['uid']))
            user = Account.objects.get(pk=uid)

            token_verified = account_activation_token.check_token(user, attrs['token'])

            if not token_verified:
                raise serializers.ValidationError({'non_field_errors': ['Invalid token!']})

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        if attrs['email'] is not None:
            try:
                user = Account.objects.get(email=attrs['email'])
            except Account.DoesNotExist:
                raise serializers.ValidationError({'email': 'Email does not exist!'})

            if user:
                uid = urlsafe_base64_encode(force_bytes(user.id))
                already_sent_mail = ForgotPasswordModel.objects.filter(uid=uid).exists()
                if already_sent_mail:
                    raise serializers.ValidationError(
                        {'email': 'You already sent email confirmation. Please check your email.'})
                sent_reset_password_email(user)
            else:
                raise serializers.ValidationError({'email': 'Email does not exist!'})
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = ForgotPasswordModel
        fields = ['uid', 'token', 'password', 'confirm_password']

    def validate(self, attrs):
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be more than 8 characters."})

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        if attrs['uid'] is not None and attrs['token'] is not None:
            forgot_user = ForgotPasswordModel.objects.filter(uid=attrs['uid'], token=attrs['token']).exists()

            if not forgot_user:
                raise serializers.ValidationError({'non_field_errors': ['Token or uid is invalid!']})

            uid = force_str(urlsafe_base64_decode(attrs['uid']))

            user = Account.objects.get(pk=uid)

            token_verified = account_activation_token.check_token(user, attrs['token'])

            if not token_verified:
                raise serializers.ValidationError({'non_field_errors': ['Invalid token!']})

        return attrs
