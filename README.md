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

🚀 Installation en local

1. Cloner le projet

git clone https://github.com/fari-code/Authentification-Sur-Mesure-sous-Django.git
cd TON_REPO

2. Créer un environnement virtuel

python -m venv env
source env/bin/activate        # Linux / Mac
# ou
env\Scripts\activate           # Windows

3. Installer les dépendances

pip install -r requirements.txt

4. Configurer les variables d'environnement

Crée un fichier .env à la racine :

SECRET_KEY=ton-secret-key-tres-longue
DEBUG=True

# Base de données (PostgreSQL local ou SQLite)
DATABASE_URL=postgres://user:password@localhost:5432/nom_db

# Email (Gmail)
EMAIL_HOST_USER=tonemail@gmail.com
EMAIL_HOST_PASSWORD=ton-mot-de-passe-application
DEFAULT_FROM_EMAIL=Authentification <tonemail@gmail.com>

# Google OAuth
GOOGLE_CLIENT_ID=ton-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=ton-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/google/callback/

5. Migrations

python manage.py makemigrations
python manage.py migrate

6. Lancer le serveur

python manage.py runserver

Ouvre http://127.0.0.1:8000



🔑 Google OAuth – Configuration





Va sur Google Cloud Console



Crée un projet



OAuth consent screen → External



Credentials → OAuth Client ID → Web application



Ajoute les Redirect URIs :





http://127.0.0.1:8000/google/callback/



http://localhost:8000/google/callback/



Copie le Client ID et Client Secret dans ton .env



🌐 Déploiement sur Render (Gratuit)

Fichiers nécessaires





requirements.txt




Étapes





Pousse le projet sur GitHub



Crée un Web Service sur Render



Crée une base PostgreSQL (plan Free)



Ajoute les variables d'environnement



Build Command : ./build.sh



Start Command : gunicorn authentification.wsgi:application

Variables d'environnement sur Render







Key



Description





SECRET_KEY



Clé secrète Django





DEBUG



False





DATABASE_URL



URL de la base PostgreSQL Render





EMAIL_HOST_USER



Email Gmail





EMAIL_HOST_PASSWORD



Mot de passe d'application Gmail





DEFAULT_FROM_EMAIL



Expéditeur des emails





GOOGLE_CLIENT_ID



Client ID Google





GOOGLE_CLIENT_SECRET



Client Secret Google





GOOGLE_REDIRECT_URI



https://ton-app.onrender.com/google/callback/



📧 Email de réinitialisation





Token valide pendant 5 minutes



Email HTML professionnel avec logo



Bouton de réinitialisation stylé



🛡️ Sécurité





Mots de passe hashés avec bcrypt



Tokens de réinitialisation à usage unique + expiration



Protection CSRF



Sessions sécurisées



Messages d'erreur génériques (anti-énumération d'emails)



👨‍💻 Auteur

Farid Dossa
Projet d'authentification custom Django



📝 Licence

Ce projet est open-source. Tu peux le modifier et l'utiliser librement.



