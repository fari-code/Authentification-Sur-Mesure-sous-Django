from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse

from authentification import settings
from .models import User
from .decorators import login_required
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone

# Create your views here.


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé")
            return redirect("register")
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        messages.success(request, "Compte créé avec succès ! Connectez-vous.")
        return redirect("login")
    return (request, HttpResponse("hello"))


