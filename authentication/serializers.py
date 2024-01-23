from rest_framework import serializers

from authentication.models import Account


class EmptySerializer(serializers.Serializer):
    pass


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'student_id', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        student_id = attrs.get('student_id')
        password = attrs.get('password')
