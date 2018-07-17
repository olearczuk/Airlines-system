"""Views module"""
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from system.flights.models import Flight, Airplane, Airport, Crew
from system.api.serializers import FlightSerializer, AirplaneSerializer, \
    AirportSerializer, CrewSerializer



class FlightViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """FlightViewSet"""
    queryset = Flight.objects.order_by("-departure_time")
    serializer_class = FlightSerializer

    def partial_update(self, request, *args, **kwargs):
        flight = self.get_object()
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        crew_id = request.data['crew']
        crew = Crew.objects.get(pk=crew_id)
        flight.crew = crew
        try:
            flight.full_clean()
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(flight, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AirportViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """AirportViewSet"""
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """AirplaneViewSet"""
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet): # pylint: disable=too-many-ancestors
    """CrewViewSet"""
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['GET'])
def user_detail(request):
   username = request.user.username
   return JsonResponse({'username': username})