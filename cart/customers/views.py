from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Customer

def sign_out(request):
    logout(request)
    return redirect('home')

def account(request):

    context = {}

    # Registration
    if request.method == "POST" and "register" in request.POST:

        context['register'] = True

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "account.html", context)

        try:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            Customer.objects.create(
                user=user,
                name=username,
                phone=phone
            )

            messages.success(request, "Registration successful!")

        except Exception as e:
            print("REGISTRATION ERROR:", e)
            messages.error(request, f"Error: {e}")

        return render(request, "account.html", context)


    # Login
    if request.method == "POST" and "login" in request.POST:

        context['register'] = False

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")

        else:
            messages.error(request, "Invalid username or password.")

        return render(request, "account.html", context)


    return render(request, "account.html", context)