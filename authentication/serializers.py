from rest_framework import serializers

from authentication.models import Account, EmailConfirmationModel
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
