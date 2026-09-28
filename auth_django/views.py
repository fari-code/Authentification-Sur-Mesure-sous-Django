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
            user = User.objects.filter(email=email).first()

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

    return render(request,"forgot_password.html")


# def password_reset_confirm(request, token):
#     try:
#         user = User.objects.get(reset_token=token)
#     except User.DoesNotExist:
#         messages.error(request, "Lien invalide ou expiré.")
#         return redirect("password_reset")

#     # Vérifier la validité du token
#     if not user.is_reset_token_valid(token):
#         messages.error(request, "Ce lien a expiré. Veuillez refaire une demande.")
#         user.clear_reset_token()
#         return redirect("password_reset")

#     if request.method == "POST":
#         password = request.POST.get("password")
#         password2 = request.POST.get("password2")

#         if not password or len(password) < 8:
#             messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
#             return render(request, "reset-password.html", {"token": token})

#         if password != password2:
#             messages.error(request, "Les mots de passe ne correspondent pas.")
#             return render(request, "reset-password.html", {"token": token})

#         # Tout est bon → on change le mot de passe
#         user.set_password(password)
#         user.clear_reset_token()          # On invalide le token
#         user.save()

#         messages.success(request, "Votre mot de passe a été modifié avec succès. Vous pouvez vous connecter.")
#         return redirect("login")

#     return render(request, "reset-password.html", {"token": token})

def password_reset_confirm(request, token):

    print("TOKEN REÇU :", repr(token))

    try:
        user = User.objects.get(reset_token=token)

        print("UTILISATEUR TROUVÉ :", user.email)
        print("TOKEN EN BASE :", repr(user.reset_token))
        print("EXPIRATION :", user.reset_token_expires)

    except User.DoesNotExist:

        print("❌ AUCUN UTILISATEUR POUR CE TOKEN")

        # Vérification supplémentaire
        users = User.objects.exclude(reset_token__isnull=True)

        for u in users:
            print(
                "TOKEN EN BASE :",
                repr(u.reset_token),
                "EMAIL :",
                u.email
            )

        messages.error(request, "Lien invalide ou expiré.")
        return redirect("password_reset")

    if not user.is_reset_token_valid(token):

        print("❌ TOKEN EXPIRÉ OU INVALIDE")

        messages.error(
            request,
            "Ce lien a expiré. Veuillez refaire une demande."
        )

        user.clear_reset_token()

        return redirect("password_reset")

    print("✅ TOKEN VALIDE")

    if request.method == "POST":

        password = request.POST.get("password", "")
        password2 = request.POST.get("password2", "")

        if not password or len(password) < 8:
            messages.error(
                request,
                "Le mot de passe doit contenir au moins 8 caractères."
            )
            return render(
                request,
                "reset-password.html",
                {"token": token}
            )

        if password != password2:
            messages.error(
                request,
                "Les mots de passe ne correspondent pas."
            )
            return render(
                request,
                "reset-password.html",
                {"token": token}
            )

        user.set_password(password)
        user.clear_reset_token()

        messages.success(
            request,
            "Votre mot de passe a été modifié avec succès."
        )

        return redirect("login")

    return render(
        request,
        "reset-password.html",
        {"token": token}
    )