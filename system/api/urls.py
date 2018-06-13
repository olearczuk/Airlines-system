from django.conf.urls import url
from django.urls import include
from rest_framework import routers
from system.api.views import FlightViewSet, CrewViewSet, AirplaneViewSet, AirportViewSet

router = routers.DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'airports', AirportViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
