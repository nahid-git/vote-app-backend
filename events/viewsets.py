from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Event
from .serializers import EventsSerializer


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    # permission_classes = [IsAuthenticated]

    # @property
    # def get_permissions(self):
    #     if self.action in ['destroy']:
    #         self.permission_classes = [IsAdminUser]
    #     elif self.action in ['list', 'retrieve']:
    #         self.permission_classes = [AllowAny]
    #     return super().get_permissions()

    @action(detail=False, methods=['GET'], url_name='my-event')
    def my_event(self, request):
        queryset = Event.objects.filter(accounts=request.user)
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
