from rest_framework import serializers
from ..flights.models import Flight, Airport, Airplane, Crew


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('country', 'city')


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ('official_number', 'capacity')


class FlightSerializer(serializers.ModelSerializer):
    final_airport = AirportSerializer(many=False, read_only=True)
    start_airport = AirportSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = ('departure_time', 'arrival_time', 'airplane', 'crew',
                  'final_airport', 'start_airport', 'id')


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ('captainsName', 'captainsSurname', 'id')
