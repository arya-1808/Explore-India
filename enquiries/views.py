from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Enquiry
import json

def enquiry(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        subject = request.POST.get("subject")
        enquiry_type = request.POST.get("enquiry_type")
        message = request.POST.get("message")

        # Save enquiry
        Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            enquiry_type=enquiry_type,
            subject=subject,
            message=message
        )

        # Send email to admin
        send_mail(
            subject=f"New Enquiry: {subject}",

            message=f"""
New enquiry received from Explore India.

Name: {name}
Email: {email}
Phone: {phone}
Enquiry Type: {enquiry_type}
Subject: {subject}

Message:
{message}
""",

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                settings.ADMIN_EMAIL
            ],

            fail_silently=False,
        )

        messages.success(
            request,
            "Your enquiry has been submitted successfully!"
        )

        return redirect("enquiry")

    return render(request,"admin/manage_enquiries.html")
# =========================
# CREATE ENQUIRY
# =========================

def create_enquiry(request):

    if request.method == "POST":

        try:
            data = json.loads(request.body)

            name = data.get("name")
            email = data.get("email")
            subject = data.get("subject")
            message = data.get("message")

            # Save enquiry in database
            enquiry = Enquiry.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Send email to admin/project Gmail
            send_mail(
                subject=f"New Enquiry: {subject}",

                message=f"""
New enquiry received from Explore India.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
""",

                from_email=settings.DEFAULT_FROM_EMAIL,

                recipient_list=[
                    settings.ADMIN_EMAIL
                ],

                fail_silently=False,
            )

            return JsonResponse({
                "success": True,
                "message": "Enquiry submitted successfully!"
            })

        except Exception as e:

            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=400)

    return JsonResponse({
        "error": "POST request required"
    }, status=405)


# =========================
# GET ALL ENQUIRIES
# =========================

def enquiry_list(request):

    enquiries = Enquiry.objects.all().values()

    return JsonResponse(
        list(enquiries),
        safe=False
    )


# =========================
# REPLY TO ENQUIRY
# =========================

def reply_enquiry(request, id):

    if request.method == "POST":

        enquiry = get_object_or_404(
            Enquiry,
            id=id
        )

        data = json.loads(request.body)

        enquiry.reply = data.get("reply")
        enquiry.save()

        return JsonResponse({
            "message": "Reply saved successfully"
        })

    return JsonResponse({
        "error": "POST request required"
    })