from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()

    ai_reply = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        default="Answered"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username