from rest_framework import viewsets
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response(serializer.data)
