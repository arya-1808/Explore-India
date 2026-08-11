from django.db import models
from django.conf import settings
from destinations.models import Destination


class Review(models.Model):

    TRAVEL_TYPE_CHOICES = [
        ('solo', 'Solo Travel'),
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('couple', 'Couple'),
        ('group', 'Group'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField()

    title = models.CharField(
        max_length=200
    )

    review_text = models.TextField()

    travel_type = models.CharField(
        max_length=20,
        choices=TRAVEL_TYPE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} - {self.destination.name}"

    class Meta:
        ordering = ['-created_at']