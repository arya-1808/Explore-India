from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count

from .models import Review
from destinations.models import Destination


# =========================
# USER REVIEW PAGE
# =========================
@login_required
def user_reviews(request):

    reviews = Review.objects.select_related(
        'user',
        'destination'
    ).all()

    # =========================
    # FILTERS
    # =========================

    rating = request.GET.get('rating')
    destination = request.GET.get('destination')
    travel_type = request.GET.get('travel_type')

    if rating:
        reviews = reviews.filter(
            rating=rating
        )

    if destination:
        reviews = reviews.filter(
            destination_id=destination
        )

    if travel_type:
        reviews = reviews.filter(
            travel_type=travel_type
        )

    # =========================
    # REVIEW STATISTICS
    # =========================

    stats = Review.objects.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    average_rating = round(
        stats['average_rating'] or 0,
        1
    )

    total_reviews = stats['total_reviews'] or 0

    # =========================
    # RATING COUNTS
    # =========================

    rating_counts = {
        5: Review.objects.filter(rating=5).count(),
        4: Review.objects.filter(rating=4).count(),
        3: Review.objects.filter(rating=3).count(),
        2: Review.objects.filter(rating=2).count(),
        1: Review.objects.filter(rating=1).count(),
    }

    destinations = Destination.objects.all()

    context = {
        'reviews': reviews,

        'destinations': destinations,

        'travel_types':
            Review.TRAVEL_TYPE_CHOICES,

        'average_rating':
            average_rating,

        'total_reviews':
            total_reviews,

        'rating_counts':
            rating_counts,
    }

    return render(
        request,
        'reviews/user_reviews.html',
        context
    )


# =========================
# ADD REVIEW
# =========================

@login_required
def add_review(request):

    if request.method == 'POST':

        destination_id = request.POST.get('destination')
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        review_text = request.POST.get('review_text')
        travel_type = request.POST.get('travel_type')

        destination = get_object_or_404(
            Destination,
            id=destination_id
        )

        Review.objects.create(
            user=request.user,
            destination=destination,
            rating=rating,
            title=title,
            review_text=review_text,
            travel_type=travel_type
        )

        messages.success(
            request,
            'Your review has been submitted successfully!'
        )

        return redirect('reviews:user_reviews')

    destinations = Destination.objects.all()

    return render(
        request,
        'reviews/add_review.html',
        {
            'destinations': destinations,
            'travel_types': Review.TRAVEL_TYPE_CHOICES,
        }
    )


# =========================
# ADMIN REVIEW PAGE
# =========================

@login_required
def admin_reviews(request):

    # Only staff/admin can access
    if not request.user.is_staff:
        return redirect('reviews:user_reviews')

    reviews = Review.objects.select_related(
        'user',
        'destination'
    ).all()

    stats = Review.objects.aggregate(
        average_rating=Avg('rating'),
        total_reviews=Count('id')
    )

    rating_counts = {
        5: Review.objects.filter(rating=5).count(),
        4: Review.objects.filter(rating=4).count(),
        3: Review.objects.filter(rating=3).count(),
        2: Review.objects.filter(rating=2).count(),
        1: Review.objects.filter(rating=1).count(),
    }

    context = {
        'reviews': reviews,

        'average_rating': round(
            stats['average_rating'] or 0,
            1
        ),

        'total_reviews': stats['total_reviews'] or 0,

        'rating_counts': rating_counts,
    }

    return render(
        request,
        'reviews/admin_reviews.html',
        context
    )


# =========================
# DELETE REVIEW
# =========================

@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id
    )

    # Admin can delete any review
    if request.user.is_staff:

        if request.method == 'POST':
            review.delete()

            messages.success(
                request,
                'Review deleted successfully!'
            )

    # Normal user can delete only their own review
    elif review.user == request.user:

        if request.method == 'POST':
            review.delete()

            messages.success(
                request,
                'Your review has been deleted!'
            )

    return redirect(
        'reviews:admin_reviews'
        if request.user.is_staff
        else 'reviews:user_reviews'
    )