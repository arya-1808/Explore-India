from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from destinations.models import Destination
from .models import Trip
from django.contrib import messages


@login_required
def trip_list(request):
    trips = Trip.objects.filter(
        user=request.user
    ).select_related("destination")

    return render(
        request,
        "trips/trip_list.html",
        {
            "trips": trips,
        }
    )

def create_trip(request):

    # User must be logged in
    if not request.user.is_authenticated:

        messages.warning(
            request,
            "🔒 Please login or create an account to create your trip."
        )

        return redirect('/accounts/login/')

    # Your existing code below
    destinations = Destination.objects.all()

    if request.method == 'POST':

        trip_name = request.POST.get('trip_name')
        destination_id = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        number_of_people = request.POST.get('number_of_people')
        budget = request.POST.get('budget')
        itinerary = request.POST.get('itinerary')
        additional_notes = request.POST.get('additional_notes')

        destination = Destination.objects.get(id=destination_id)

        Trip.objects.create(
            user=request.user,
            trip_name=trip_name,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            number_of_people=number_of_people,
            budget=budget,
            itinerary=itinerary,
            additional_notes=additional_notes
        )

        messages.success(
            request,
            "🎉 Your trip has been created successfully!"
        )

        return redirect('trips:trip_list')

    return render(
        request,
        'trips/create_trip.html',
        {
            'destinations': destinations
        }
    )


@login_required
def trip_detail(request, id):
    trip = get_object_or_404(
        Trip,
        id=id,
        user=request.user
    )

    return render(
        request,
        "trips/trip_detail.html",
        {"trip": trip}
    )


@login_required
def edit_trip(request, id):
    trip = get_object_or_404(
        Trip,
        id=id,
        user=request.user
    )

    destinations = Destination.objects.all()

    if request.method == "POST":

        trip.trip_name = request.POST.get("trip_name")
        trip.destination_id = request.POST.get("destination")
        trip.start_date = request.POST.get("start_date")
        trip.end_date = request.POST.get("end_date")
        trip.number_of_people = request.POST.get("number_of_people")
        trip.budget = request.POST.get("budget")
        trip.itinerary = request.POST.get("itinerary")
        trip.notes = request.POST.get("notes")

        trip.save()

        return redirect("trips:trip_detail", id=trip.id)

    return render(
        request,
        "trips/edit_trip.html",
        {
            "trip": trip,
            "destinations": destinations,
        }
    )


@login_required
def delete_trip(request, id):
    trip = get_object_or_404(
        Trip,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        trip.delete()
        return redirect("trips:trip_list")

    return render(
        request,
        "trips/delete_trip.html",
        {"trip": trip}
    )