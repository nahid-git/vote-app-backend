from django.db.models import Count
from rest_framework import serializers

from events.models import VoterSelectedOption
from options.serializers import OptionSerializer
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    question_total_votes = serializers.SerializerMethodField()
    option_votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'event', 'question_total_votes', 'option_votes_count', 'options']

    def get_question_total_votes(self, obj):
        total_votes = VoterSelectedOption.objects.filter(question_id=obj).count()
        return total_votes

    def get_option_votes_count(self, obj):
        option_counts = (
            VoterSelectedOption.objects.filter(question_id=obj)
            .values('selected_option')
            .annotate(count=Count('selected_option'))
        )

        result = [{item['selected_option']: item['count']} for item in option_counts]
        return result
