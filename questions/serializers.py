from rest_framework import serializers

from events.models import VoterSelectedOption
from options.serializers import OptionSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    question_total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'event', 'question_total_votes', 'options']

    def get_question_total_votes(self, obj):
        total_votes = VoterSelectedOption.objects.filter(question_id=obj).count()
        return total_votes
