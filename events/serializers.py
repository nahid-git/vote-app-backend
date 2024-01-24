from rest_framework import serializers

from questions.serializers import QuestionSerializer
from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'questions']
