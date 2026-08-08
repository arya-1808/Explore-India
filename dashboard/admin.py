from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'destination',
        'booking_date',
        'persons',
        'status',
    )

    list_filter = (
        'status',
        'booking_date',
    )

    search_fields = (
        'user__username',
        'destination__name',
    )
