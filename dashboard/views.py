from django.contrib.auth.models import User
from django.shortcuts import render
from destinations.models import Destination
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    #search functionality for recent destinations
    search = request.GET.get("search")
    recent_destinations = Destination.objects.order_by("-created_at")
    if search:
        recent_destinations = recent_destinations.filter(
        name__icontains=search
    )
    recent_destinations = recent_destinations[:5]
    
#dashboard statistics
    total_destinations = Destination.objects.count()

    featured_destinations = Destination.objects.filter(
        is_featured=True
    ).count()

    recent_destinations = Destination.objects.order_by(
        '-created_at'
    )[:5]

    total_users = User.objects.count()
    context = {
        "total_destinations": total_destinations,
        "featured_destinations": featured_destinations,
        "recent_destinations": recent_destinations,
        "total_users": total_users,
    }

    return render(request, "dashboard/dashboard.html", context)

def edit_destination(request, id):
    destination = get_object_or_404(Destination, id=id)

    if request.method == "POST":
        destination.name = request.POST.get("name")
        destination.description = request.POST.get("description")
        destination.category = request.POST.get("category")
        destination.state = request.POST.get("state")
        destination.city = request.POST.get("city")
        destination.best_time_to_visit = request.POST.get("best_time")
        destination.avg_budget_per_day = request.POST.get("budget")

        # Image update (optional)
        if request.FILES.get("image"):
            destination.image = request.FILES["image"]

        destination.save()
        return redirect("dashboard:dashboard")

    context = {
        "destination": destination,
    }

    return render(request, "dashboard/edit_destination.html", context)


def delete_destination(request, id):
    destination = get_object_or_404(Destination, id=id)

    destination.delete()

    return redirect("dashboard:dashboard")