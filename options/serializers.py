from rest_framework import serializers

from events.models import VoterSelectedOption
from .models import Option


class OptionSerializer(serializers.ModelSerializer):
    option_total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Option
        fields = ['id', 'title', 'option_total_votes']

    def get_option_total_votes(self, obj):
        total_votes = VoterSelectedOption.objects.filter(selected_option_id=obj).count()
        return total_votes
