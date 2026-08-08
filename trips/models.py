from django.db import models
from destinations.models import Destination
from django.contrib.auth.models import User


class Trip(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    trip_name = models.CharField(max_length=150)

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    start_date = models.DateField()
    end_date = models.DateField()

    number_of_people = models.PositiveIntegerField(default=1)

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    itinerary = models.TextField(
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.trip_name
