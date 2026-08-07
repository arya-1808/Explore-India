from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Destination, CATEGORY_CHOICES, STATE_CHOICES


def destination_list(request):
    destinations = Destination.objects.all()

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    state = request.GET.get('state', '')

    if query:
        destinations = destinations.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        destinations = destinations.filter(category=category)

    if state:
        destinations = destinations.filter(state=state)

    featured_destinations = Destination.objects.filter(is_featured=True)

    context = {
    'destinations': destinations,
    'featured_destinations': featured_destinations,
    'categories': CATEGORY_CHOICES,
    'states': STATE_CHOICES,
    'selected_category': category,
    'selected_state': state,
    'query': query,
}

    return render(request, "destinations/destination_list.html", context)

def destination_detail(request, slug):
    
    destination = get_object_or_404(Destination, slug=slug)

    related_destinations = Destination.objects.filter(
        category=destination.category
    ).exclude(id=destination.id)[:3]

    context = {
        "destination": destination,
        "related_destinations": related_destinations,
    }

    return render(
        request,
        "destinations/destination_detail.html",
        context,
    )