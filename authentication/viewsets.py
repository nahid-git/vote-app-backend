from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from authentication.serializers import SignupSerializer, EmptySerializer


class AuthenticationViewSet(viewsets.ModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'signup':
            return SignupSerializer
        return EmptySerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
