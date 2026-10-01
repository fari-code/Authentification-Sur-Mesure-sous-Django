import secrets
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
        password = request.POST.get("password", "")
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                # store the ID in the session
                request.session["user_id"] = user.id
                request.session["user_email"] = user.email
                user.last_login = timezone.now()
                user.save()
                messages.success(request, "Connexion réussie !")
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

        user = User.objects.filter(email=email).first()

        if user:
            # Générer le token
            token = user.generate_reset_token()
            reset_link = request.build_absolute_uri(f"/reset-password/{token}/")

            # Contexte pour le template email
            context = {
                "first_name": user.first_name,
                "reset_link": reset_link,
            }

            html_content = render_to_string("emails/password_reset.html", context)

            text_content = strip_tags(html_content)

            # Envoyer l'email
            email_message = EmailMultiAlternatives(
                subject="Réinitialisation de votre mot de passe",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)

        messages.success(
            request, "Si cet email existe, un lien de réinitialisation a été envoyé."
        )
        return redirect("password_reset")

    return render(request, "forgot_password.html")


def password_reset_confirm(request, token):
    try:
        user = User.objects.get(reset_token=token)
    except User.DoesNotExist:
        messages.error(request, "Lien invalide ou expiré.")
        return redirect("password_reset")

    # Vérifier la validité du token
    if not user.is_reset_token_valid(token):
        messages.error(request, "Ce lien a expiré. Veuillez refaire une demande.")
        user.clear_reset_token()
        return redirect("password_reset")

    if request.method == "POST":
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if not password or len(password) < 8:
            messages.error(
                request, "Le mot de passe doit contenir au moins 8 caractères."
            )
            return render(request, "reset-password.html", {"token": token})

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "reset-password.html", {"token": token})

        # Tout est bon → on change le mot de passe
        user.set_password(password)
        user.clear_reset_token()  # On invalide le token
        user.save()

        messages.success(
            request,
            "Votre mot de passe a été modifié avec succès. Vous pouvez vous connecter.",
        )
        return redirect("login")

    return render(request, "reset-password.html", {"token": token})


def google_login(request):
    # On génère un state pour la sécurité (CSRF)
    state = secrets.token_urlsafe(16)
    request.session["google_oauth_state"] = state

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        "scope=openid%20email%20profile&"
        f"state={state}&"
        "access_type=online&"
        "prompt=select_account"
    )
    return redirect(google_auth_url)


def google_callback(request):
    # Vérification du state (sécurité)
    state = request.GET.get("state")
    if state != request.session.get("google_oauth_state"):
        messages.error(request, "Erreur de sécurité. Réessayez.")
        return redirect("login")

    code = request.GET.get("code")
    if not code:
        messages.error(request, "Connexion Google annulée.")
        return redirect("login")

    # 1. Échanger le code contre un access_token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        messages.error(request, "Erreur lors de la connexion Google.")
        return redirect("login")

    access_token = token_json["access_token"]

    # 2. Récupérer les infos de l'utilisateur
    userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo = userinfo_response.json()

    email = userinfo.get("email")
    first_name = userinfo.get("given_name", "")
    last_name = userinfo.get("family_name", "")
    google_id = userinfo.get("sub")  # ID unique Google

    if not email:
        messages.error(request, "Impossible de récupérer l'email Google.")
        return redirect("login")

    # 3. Créer ou récupérer l'utilisateur
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            # On génère un mot de passe aléatoire (l'utilisateur ne s'en servira pas)
            "auth_provider": "google",
            "password":"",
        },
    )

    # Si le compte existait déjà mais sans nom, on le met à jour
    if not created:
        if not user.first_name:
            user.first_name = first_name
        if not user.last_name:
            user.last_name = last_name
        user.save()

    # 4. Connecter l'utilisateur (mettre dans la session)
    request.session["user_id"] = user.id
    request.session["user_email"] = user.email
    user.last_login = timezone.now()
    user.save()

    messages.success(request, f"Bienvenue {user.first_name} !")
    return redirect("dashboard")
