from django.contrib import admin
from .models import Passenger, Airplane, Airport, Crew, Flight, Ticket

admin.site.register([Passenger, Airplane, Airport, Crew, Flight, Ticket])