import pytz
from dateutil.parser import parse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_GET, require_http_methods

from system.flights.forms import PassengerForm
from system.flights.models import Flight, Passenger, Ticket


@require_GET
def flights_view(request):
    if request.method == 'GET':
        departure = request.GET.get("departure_time")
        arrival = request.GET.get("arrival_time")
        flights = Flight.objects.order_by('-departure_time').all()
        was_err = False
        if departure and arrival:
            try:
                dep_time = parse(departure).replace(tzinfo=pytz.utc)
                arr_time = parse(arrival).replace(tzinfo=pytz.utc)
            except Exception:
                was_err = True
                return render(request, template_name="flights_list.html", context=locals())

            flights = flights.filter(departure_time__gte=dep_time, arrival_time__lte=arr_time)\
                .order_by('-departure_time').all()
        return render(request, template_name="flights_list.html", context=locals())


@require_http_methods(["GET", "POST"])
def flight_view(request, flight_id):
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
            reserved = Ticket.objects.filter(flight=flight).count()
            available = flight.airplane.capacity

            request.session["add_info"] = "No more seats!"

            if reserved < available:
                err = False
                passenger = Passenger.objects.create(name=form.cleaned_data["name"],
                                                     surname=form.cleaned_data["surname"])
                ticket = Ticket(flight=flight, passenger=passenger)
                ticket.full_clean()
                ticket.save()
                request.session["add_info"] = "Done!"

            return redirect(to=request.path)
        else:
            request.session["add_info"] = "This passenger already booked a seat for this flight."
            return redirect(to=request.path)
