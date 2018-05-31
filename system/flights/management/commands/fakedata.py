from django.core.management import BaseCommand
from django.db import transaction
from system.flights.models import Airplane, Airport, Flight
from faker import Faker
from random import random, randint, choice, shuffle
from pytz import timezone
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

        for i in range(50):
            name = fake.random_number()
            capacity = 20 + randint(0, 50)

            airplane = Airplane(official_number=name, capacity=capacity)
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

        tz = timezone('Europe/Warsaw')
        shuffle(airplanes)
        for airplane in airplanes:
            d_time = tz.localize(fake.date_time())

            for i in range(4):
                a_time = d_time + timedelta(hours=randint(1, 5))
                flight = Flight(start_airport=choice(airports),
                                final_airport=choice(airports),
                                airplane=airplane,
                                departure_time=d_time,
                                arrival_time=a_time)
                flight.full_clean()
                flight.save()
                d_time += timedelta(days=randint(1, 60))

    def handle(self, *args, **options):
        self.generate_data()

