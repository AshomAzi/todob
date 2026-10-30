from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def signup(request):

    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if username is not None and email is not None:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"{username} is already taken!")
                return redirect("signup")
            if User.objects.filter(email=email).exists():
                messages.error(request, f"{email} is already taken!")
                return redirect("signup")
            if len(password1) < 8:
                messages.error(request, "Password must be at least 8 characters")
                return redirect("signup")
            
            if password1 != password2:
                messages.error(request, "Password does not match")
                return redirect("signup")
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            user.save()
            return redirect("signin")
        else:
            messages.error(request, "Fields cannot be empty!")
            return redirect("signup")

    else:
        return render(request, "signup.html")