from rest_framework import serializers

from options.serializers import OptionSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'event', 'options']
