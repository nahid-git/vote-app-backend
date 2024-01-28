from datetime import datetime

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import Account, EmailConfirmationModel, ForgotPasswordModel
from authentication.serializers import SignupSerializer, EmptySerializer, EmailVerifySerializer, LoginSerializer, \
    ResetPasswordSerializer, ForgotPasswordSerializer


class AuthenticationViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset = []

    def get_serializer_class(self):
        if self.action == 'signup':
            return SignupSerializer
        elif self.action == 'verify':
            return EmailVerifySerializer
        elif self.action == 'login':
            return LoginSerializer
        elif self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        return EmptySerializer

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='signup')
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Please confirm your email address to complete the registration'})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = Account.objects.get(email=serializer.data['email'])
            user.last_login = datetime.now()
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'token': str(refresh.access_token),
                'email': user.email,
                'user_id': user.id
            })
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'], url_path='verify')
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_id = force_str(urlsafe_base64_decode(serializer.data['uid']))

            user = Account.objects.get(pk=user_id)
            user.is_active = True
            user.save()

            get_user_data = EmailConfirmationModel.objects.filter(uid=serializer.data['uid'])
            get_user_data.delete()

            return Response({'message': 'Your account has been activated successfully.'}, status=status.HTTP_200_OK)
        return Response({'non_field_errors': ['Activation link is invalid!']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['POST'], url_path='forgot_password')
    def forgot_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response({'message': 'Please check your email and reset password.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'], url_path='reset_password')
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user_id = force_str(urlsafe_base64_decode(serializer.data['uid']))

            user = Account.objects.get(pk=user_id)
            user.set_password(serializer.data['password'])
            user.save()

            get_user_data = ForgotPasswordModel.objects.filter(uid=serializer.data['uid'])
            get_user_data.delete()

            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response({'non_field_errors': ['Password reset link is invalid!']},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
