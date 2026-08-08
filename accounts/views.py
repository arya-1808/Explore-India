from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
import random

def user_login(request):
  
    if request.method == "POST":
       
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_home")
        else:
            return render(request, "users/login.html", {"error": "Invalid username or password"})

    return render(request, "users/login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "users/register.html")

from destinations.models import Destination


def user_home(request):

    query = request.GET.get("q", "")

    destinations = Destination.objects.all()

    if query:
        destinations = destinations.filter(
            name__icontains=query
        )

    return render(
        request,
        "users/home.html",
        {
            "popular_destinations": destinations[:6],
            "search_results": destinations,
            "query": query,
        }
    )

def user_logout(request):
    logout(request)
    return redirect("user_home")


@login_required
def profile(request):
    if request.method == "POST":
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.save()   # Save changes to the database

    return render(request, "users/profile.html")
@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()

        # Username and email can be displayed but not changed here
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "users/edit_profile.html")


def forgot_password(request):
    print("view called")

    if request.method == "POST":

        # SEND OTP
        if request.POST.get("send_otp"):
            print("post request received")

            email = request.POST.get("email")

            print("EMAIL =", email)

            try:
                user = User.objects.get(email=email)

                otp = random.randint(100000, 999999)

                request.session["reset_email"] = email
                request.session["reset_otp"] = str(otp)

                print("OTP =", otp)

                send_mail(
                    subject="Password Reset OTP",
                    message=f"Your OTP is {otp}",
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent successfully.")

            except User.DoesNotExist:
                messages.error(request, "Email not registered.")

            except Exception as e:
                print(e)
                messages.error(request, str(e))

            return render(
                request,
                "users/forgot_password.html",
                {"email": email},
            )

        # VERIFY OTP
        elif request.POST.get("verify_otp"):

            otp = request.POST.get("otp")

            if otp == request.session.get("reset_otp"):
                return redirect("change_password")

            else:
                messages.error(request, "Invalid OTP")

            return render(
                request,
                "users/forgot_password.html",
                {
                    "email": request.session.get("reset_email")
                },
            )

    return render(request, "users/forgot_password.html")
                

    


def change_password(request):

    # Forgot Password Flow
    if "reset_email" in request.session:

        email = request.session["reset_email"]
        user = User.objects.get(email=email)

        if request.method == "POST":

            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")

            else:
                user.set_password(new_password)
                user.save()

                del request.session["reset_email"]
                del request.session["reset_otp"]

                messages.success(request, "Password changed successfully.")
                return redirect("login")

        return render(request, "users/change_password.html")

    # Normal Change Password
    else:

        user = request.user

        if request.method == "POST":

            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not user.check_password(old_password):
                messages.error(request, "Old password is incorrect.")

            elif new_password != confirm_password:
                messages.error(request, "Passwords do not match.")

            else:
                user.set_password(new_password)
                user.save()

                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully.")
                return redirect("profile")

        return render(request, "users/change_password.html")

    
