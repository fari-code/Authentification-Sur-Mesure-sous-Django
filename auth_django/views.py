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

        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        email = request.POST.get("email").strip().lower()
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
        request.session["user_id"] = user.id
        request.session["user_email"] = user.email
        messages.success(request, "Compte créé avec succès !")
        return redirect("dashboard")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password","")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                # store the ID in the session
                request.session["user_id"] = user.id
                request.session["user_email"] = user.email
                user.last_login = timezone.now()
                user.save()
                return redirect("dashboard")
            else:
                messages.error(request, "Email ou mot de passe incorrect")
        except User.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect")
    return render(request, "login.html")


def logout_view(request):
    request.session.flush()  # détruit la session
    return redirect("login")


@login_required
def dashboard(request):
    user = User.objects.get(id=request.session["user_id"])
    return render(request, "dashboard.html", {"user": user})


# reset_password


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        try:
            user = User.objects.get(email=email)

            # Générer le token
            token = user.generate_reset_token()

            # Construire le lien
            reset_link = request.build_absolute_uri(f"/reset-password/{token}/")

            # Envoyer l'email
            subject = "Réinitialisation de votre mot de passe"
            message = f"""
Bonjour {user.first_name},

Vous avez demandé la réinitialisation de votre mot de passe.
Cliquez sur le lien suivant (valable 1 heure) :

{reset_link}

Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.

Cordialement,
L'équipe
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # ou "noreply@tonsite.com"
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Un email de réinitialisation a été envoyé.")
            return redirect("login")

        except User.DoesNotExist:

            messages.success(request, "Si cet email existe, un lien a été envoyé.")
            return redirect("login")

    return HttpResponse("password_reset_request.html")
