from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from ..flights.models import Flight, Crew
from rest_framework.response import Response
from ..flights.models import *
from .serializers import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.order_by("-departure_time")
    serializer_class = FlightSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # TODO select_for_update
        crew_id = request.data['crew']
        crew_flights = Flight.objects.filter(crew=crew_id, departure_time__lte=instance.arrival_time,
                                             arrival_time__gte=instance.departure_time)
        if crew_flights.exists():
            return Response(data={'message': 'This crew is not available'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

    def create(self, request, *args, **kwargs):
        print("asdfasd")
        print("auth", request.user.is_authenticated)
        print("req", request.user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)