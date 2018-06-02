"""Views for flights list and particular flight"""

# from django.http import JsonResponse
# from django.core import serializers

from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from system.flights.forms import PassengerForm, FlightForm
from system.flights.models import Flight, Passenger, Ticket
import datetime


def flights_view(request):
    """Flights view"""
    if request.method == 'GET':
        departure = request.GET.get("departure_time")
        arrival = request.GET.get("arrival_time")
        form = FlightForm()
        print("departure: ", departure)
        print("arrival: ", arrival)
        print(isinstance(departure, datetime.datetime))
        print(isinstance(arrival, datetime.datetime))

        flights = Flight.objects.order_by('-departure_time').all()

        if departure is not None and arrival is not None:
            flights = Flight.objects.filter(departure_time__gte=departure,
                                            arrival_time__lte=arrival).order_by('-departure_time')\
                                            .all()

        return render(request, template_name="flights_list.html", context=locals())
    else:
        form = FlightForm(request.POST)
        if form.is_valid():
            print("departure: ", request.POST.get("departure_time"))
            print("arrival: ", request.POST.get("arrival_time"))
        return redirect(to=request.path, context=locals())


@transaction.atomic
def flight_view(request, flight_id):
    """Flight view"""
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'GET':
        form = PassengerForm()
        passengers = flight.passengers.all()
        return render(request, template_name='flight.html', context=locals())
    else:
        form = PassengerForm(request.POST)
        if form.is_valid():
            Flight.objects.select_for_update().filter(id=flight_id)
            passenger = Passenger(name=form.cleaned_data["name"],
                                  surname=form.cleaned_data["surname"])
            passenger.full_clean()
            reserved = Ticket.objects.filter(flight=flight).count()
            available = flight.airplane.capacity

            err = True

            if reserved < available:
                err = False
                passenger.save()
                ticket = Ticket(flight=flight, passenger=passenger)
                ticket.full_clean()
                ticket.save()
            print("POST", err)
            # return redirect(to=request.path, was_error=err)
            return redirect(to=request.path, err=err)


def index(request):
    """Index"""
    return redirect("/flights/flights_list")
    # return render(request, "system/static/asdf.html")


