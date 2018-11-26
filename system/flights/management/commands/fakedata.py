from django.core.management import BaseCommand
from django.db import transaction
from system.flights.models import Airplane, Airport, Flight, Passenger, Ticket, Crew
from faker import Faker
from random import randint, choice, shuffle, sample
import pytz
from datetime import timedelta


class Command(BaseCommand):
    help = "Generating fake data for database"

    @transaction.atomic
    def generate_data(self):
        Flight.objects.all().delete()
        Airplane.objects.all().delete()
        Airport.objects.all().delete()
        Passenger.objects.all().delete()
        Ticket.objects.all().delete()
        Crew.objects.all().delete()

        fake = Faker()
        airplanes = []
        airports = []

        numbers = sample(range(100, 999), 50)

        for number in numbers:
            capacity = 4 + randint(0, 5)
            airplane = Airplane(official_number=number, capacity=capacity)
            airplane.full_clean()
            airplane.save()
            airplanes.append(airplane)

        for i in range(50):
            airport = Airport(city=fake.city(), country=fake.country())
            airport.full_clean()
            airport.clean()
            airport.save()
            airports.append(airport)

        shuffle(airplanes)

        for airplane in airplanes:

            d_time = fake.date_time_between(start_date='-1y', end_date='+1y', tzinfo=pytz.utc)
            a_time = d_time + timedelta(hours=randint(1, 10))
            flight = Flight(start_airport=choice(airports),
                            final_airport=choice(airports),
                            airplane=airplane,
                            departure_time=d_time,
                            arrival_time=a_time)
            flight.full_clean()
            flight.save()

            d_time = fake.date_time_between(start_date=a_time, tzinfo=pytz.utc)
            a_time = d_time + timedelta(hours=randint(1, 10))
            flight = Flight(start_airport=choice(airports),
                            final_airport=choice(airports),
                            airplane=airplane,
                            departure_time=d_time,
                            arrival_time=a_time)
            flight.full_clean()
            flight.save()

    def handle(self, *args, **options):
        self.generate_data()

