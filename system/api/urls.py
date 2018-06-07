from django.conf.urls import url
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'airports', AirportViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
