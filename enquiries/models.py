from django.db import models


class Enquiry(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=15)

    enquiry_type = models.CharField(max_length=100)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    reply = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name