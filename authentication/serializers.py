from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from authentication.models import Account, EmailConfirmationModel
from authentication.token import account_activation_token
from authentication.utils import sent_user_verify_email


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
        )
        user.student_id = validated_data['student_id']
        user.set_password(validated_data['password'])
        user.save()
        sent_user_verify_email(user)

        return user


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
