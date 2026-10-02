from django.db import models
from django.utils import timezone
import bcrypt
import secrets


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=True)  # blank=True important
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    auth_provider = models.CharField(max_length=20, default="email")  # "email" ou "google"

    # for reset password
    reset_token = models.CharField(max_length=100, null=True, blank=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        """Hash le mot de passe"""
        if not raw_password:
            self.password = ""
            return

        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(
            raw_password.encode("utf-8"), salt
        ).decode("utf-8")

    def check_password(self, raw_password):
        """Vérifie le mot de passe de façon sécurisée"""
        # Si pas de mot de passe (compte Google) ou mot de passe vide
        if not self.password or not raw_password:
            return False

        try:
            return bcrypt.checkpw(
                raw_password.encode("utf-8"),
                self.password.encode("utf-8")
            )
        except (ValueError, TypeError):
            # Hash invalide → on considère que c'est faux
            return False

    def __str__(self):
        return self.email

    def generate_reset_token(self):
        """Génère un token sécurisé et fixe une expiration de 5 minutes"""
        self.reset_token = secrets.token_urlsafe(32)
        self.reset_token_expires = timezone.now() + timezone.timedelta(minutes=5)
        self.save()
        return self.reset_token

    def is_reset_token_valid(self, token):
        if self.reset_token != token:
            return False
        if not self.reset_token_expires or timezone.now() > self.reset_token_expires:
            return False
        return True

    def clear_reset_token(self):
        self.reset_token = None
        self.reset_token_expires = None
        self.save()