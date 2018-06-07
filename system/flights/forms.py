"""forms module"""
from django.forms import ModelForm
from .models import Passenger, Flight


class PassengerForm(ModelForm):
    """Passenger form"""
    class Meta:
        """Meta class"""
        model = Passenger
        fields = '__all__'


class FlightForm(ModelForm):
    """Flight form"""
    class Meta:
        """Meta class"""
        model = Flight
        fields = ['departure_time', 'arrival_time']
