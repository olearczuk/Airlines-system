"""forms module"""
from django.forms import ModelForm
from .models import Passenger


class PassengerForm(ModelForm):
    """Passenger form"""
    class Meta:
        """Meta class"""
        model = Passenger
        fields = '__all__'
