from rest_framework import serializers
from ..flights.models import Flight, Crew, Airport, Airplane, Crew


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('captainsName', 'captainsSurname', 'flights')


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('country', 'city')


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ('capacity', 'official_number')


class FlightSerializer(serializers.ModelSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    final_airport = AirportSerializer(many=False, read_only=True)
    start_airport = AirportSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)

    class Meta:
        model = Flight
        fields = ('departure_time', 'arrival_time', 'airplane', 'crew',
                  'final_airport', 'start_airport')
