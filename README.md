# 🔐 Système d'Authentification Django Custom

Système d’authentification sur-mesure sous Django développé sans django.contrib.auth. Gestion manuelle des sessions (cookies HttpOnly), hachage sécurisé (Bcrypt), réinitialisation de mot de passe et connexion Google OAuth 2.0 pure.

---

## ✨ Fonctionnalités

- ✅ Inscription (Nom, Prénom, Email, Mot de passe)
- ✅ Connexion avec Email + Mot de passe
- ✅ Connexion avec **Google OAuth**
- ✅ Mot de passe oublié (token + email HTML)
- ✅ Modification du mot de passe (utilisateur connecté)
- ✅ Dashboard protégé
- ✅ Hashage sécurisé avec **bcrypt**
- ✅ Sessions manuelles
- ✅ Design moderne avec **Tailwind CSS**

---

## 🛠️ Technologies utilisées

- Python 3.13
- Django 6.1
- PostgreSQL
- bcrypt
- Tailwind CSS
- Gunicorn + Whitenoise
- Render (déploiement)

---

## 📁 Structure du projet

```bash
authentification/
├── authentification/          # Configuration du projet
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── auth_django/               # Application principale
│   ├── models.py              # Modèle User custom
│   ├── views.py
│   ├── decorators.py
│   ├── urls.py
│   └── ...
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── forgot_password.html
│   └── emails/
│       └── password_reset.html
├── static/
├── requirements.txt
├── staticfiles
└── README.md