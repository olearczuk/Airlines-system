"""Views for flights list and particular flight"""

# from django.http import JsonResponse
# from django.core import serializers

from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from dateutil.parser import parse
from system.flights.forms import PassengerForm
from system.flights.models import Flight, Passenger, Ticket


def flights_view(request):
    """Flights view"""
    if request.method == 'GET':
        departure = request.GET.get("departure_time")
        arrival = request.GET.get("arrival_time")
        dep_time = timezone.now()
        arr_time = timezone.now()
        flights = Flight.objects.order_by('-departure_time').all()
        was_err = False
        if departure and arrival:
            try:
                dep_time = parse(departure)
                arr_time = parse(arrival)
            except Exception as e:
                print(e)
                was_err = True
                return render(request, template_name="flights_list.html", context=locals())

        if departure is not None and arrival is not None:
            flights = Flight.objects.filter(departure_time__gte=dep_time,
                                            arrival_time__lte=arr_time).order_by('-departure_time')\
                                            .all()

        return render(request, template_name="flights_list.html", context=locals())
    else:
        return redirect(to=request.path, context=locals())


@transaction.atomic
def flight_view(request, flight_id):
    """Flight view"""
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == 'GET':
        to_show = "add_info" in request.session
        info = ""
        if to_show:
            info = request.session["add_info"]
            del request.session["add_info"]
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

            request.session["add_info"] = "No more seats!"

            if reserved < available:
                err = False
                passenger.save()
                ticket = Ticket(flight=flight, passenger=passenger)
                ticket.full_clean()
                ticket.save()
                request.session["add_info"] = "Done!"

            return redirect(to=request.path)
