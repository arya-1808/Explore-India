from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    booking_date = models.DateField()
    persons = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} - {self.destination.name}"