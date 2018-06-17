"""models module"""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Passenger(models.Model):
    """Passenger class"""
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    class Meta:
        """Meta"""
        unique_together = ('name', 'surname')

    def __str__(self):
        return 'Passenger %s %s' % (self.name, self.surname)


class Airplane(models.Model):
    """Airplane class"""
    capacity = models.IntegerField(default=25)
    official_number = models.CharField(max_length=100, primary_key=True)

    def clean(self):
        if self.capacity < 0:
            raise ValidationError('Airplane can not have less than 0 seats')

    def __str__(self):
        return 'Airplane %s, capacity %s' % (self.official_number, self.capacity)


class Airport(models.Model):
    """Airport class"""
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    class Meta:
        """Meta"""
        unique_together = ('country', 'city')

    def __str__(self):
        return 'Airport located in %s (%s)' % (self.city, self.country)


class Crew(models.Model):
    """Crew class"""
    captainsName = models.CharField(max_length=150)
    captainsSurname = models.CharField(max_length=150)

    class Meta:
        """Meta"""
        unique_together = ('captainsName', 'captainsSurname')

    def __str__(self):
        return 'Crew ordered by captain %s %s' % (self.captainsName, self.captainsSurname)


class Flight(models.Model):
    """Flight class"""
    start_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                      related_name='start_airport')
    departure_time = models.DateTimeField()

    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='airplane')
    passengers = models.ManyToManyField(Passenger, through='Ticket')

    final_airport = models.ForeignKey(Airport, on_delete=models.CASCADE,
                                      related_name='final_airport')
    arrival_time = models.DateTimeField()

    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='flights',
                             default=None, null=True, blank=True)

    def clean(self):
        if self.arrival_time <= self.departure_time:
            raise ValidationError('Arrival time <= departure time')
        flights = Flight.objects.exclude(pk=self.pk)
        other_flights = flights.filter(
            departure_time__lte=self.arrival_time,
            arrival_time__gte=self.departure_time,
        )
        conflicting_flights = other_flights.select_for_update().filter(airplane=self.airplane)
        if conflicting_flights.exists():
            raise ValidationError('This flights airplane is currently busy')
        if self.crew is not None:
            if other_flights.filter(crew=self.crew).exists():
                raise ValidationError('This flights crew is currently busy')

    def __str__(self):
        return 'Flight %s -> %s' % (self.start_airport, self.final_airport)


class Ticket(models.Model):
    """Ticket class"""
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    def clean(self):
        pass_num = Ticket.objects.filter(flight=self.flight).count()
        places = self.flight.airplane.capacity
        if places == pass_num:
            raise ValidationError('No more places in airplane')
