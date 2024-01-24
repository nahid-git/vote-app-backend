from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.viewsets import AuthenticationViewSet
from events.viewsets import EventsViewSet
from options.views import OptionViewSet
from questions.views import QuestionViewSet

router = routers.DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='authentication')
router.register(r'events', EventsViewSet, basename='events')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'option', OptionViewSet, basename='option')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
