from django.core.management import BaseCommand
from django.db import transaction
from system.flights.models import Airplane, Airport, Flight
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
            city = fake.city()
            country = fake.country()
            airport = Airport(city=city, country=country)
            airport.full_clean()
            airport.clean()
            airport.save()
            airports.append(airport)

        tz = pytz.utc
        shuffle(airplanes)

        # d1 = datetime.strptime('1/1/2017 1:30 PM', '%m/%d/%Y %I:%M %p')
        # d2 = datetime.strptime('1/1/2018 4:50 AM', '%m/%d/%Y %I:%M %p')

        for airplane in airplanes:

            d_time = fake.date_time_between(start_date='-1y', tzinfo=pytz.utc)
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

