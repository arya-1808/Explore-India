from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

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


def user_home(request):
    return render(request, "users/home.html")

def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    if request.method == "POST":
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.save()   # Save changes to the database

    return render(request, "users/profile.html")

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password changed successfully.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

    return render(request, "users/forgot_password.html")


def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

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