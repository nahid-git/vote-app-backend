from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from authentication.viewsets import AuthenticationViewSet
from events.viewsets import EventsViewSet

router = routers.DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='authentication')
router.register(r'events', EventsViewSet, basename='events')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
