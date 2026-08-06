from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Enquiry
import json


def enquiry_list(request):
    enquiries = Enquiry.objects.all().values()

    return JsonResponse(list(enquiries), safe=False)


def reply_enquiry(request, id):

    if request.method == "POST":

        enquiry = get_object_or_404(Enquiry, id=id)

        data = json.loads(request.body)

        enquiry.reply = data.get("reply")
        enquiry.save()

        return JsonResponse({
            "message": "Reply sent successfully"
        })

    return JsonResponse({
        "error": "POST request required"
    })