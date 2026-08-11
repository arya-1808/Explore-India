from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'destination',
        'rating',
        'travel_type',
        'created_at',
    )

    list_filter = (
        'rating',
        'travel_type',
        'destination',
    )

    search_fields = (
        'title',
        'review_text',
        'user__username',
        'destination__name',
    )

    ordering = ('-created_at',)