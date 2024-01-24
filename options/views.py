from rest_framework import viewsets
from rest_framework.response import Response

from .models import Option
from .serializers import OptionSerializer


class OptionViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Option.objects.all()
        serializer = OptionSerializer(queryset, many=True)
        return Response(serializer.data)
