Système d'Authentification Django Custom

Système d'authentification sur-mesure sous Django développé sans django.contrib.auth. Le projet gère manuellement les sessions (cookies HttpOnly), le hachage sécurisé des mots de passe (Bcrypt), la réinitialisation de mot de passe et l'authentification Google OAuth 2.0.

Fonctionnalités

Inscription (Nom, Prénom, Email, Mot de passe)

Connexion avec Email et Mot de passe

Connexion via Google OAuth 2.0

Réinitialisation de mot de passe (génération de token et envoi d'email HTML)

Modification du mot de passe pour les utilisateurs connectés

Dashboard protégé

Hachage sécurisé avec Bcrypt

Gestion manuelle des sessions utilisateur

Interface moderne conçue avec Tailwind CSS

Technologies utilisées

Python 3.13

Django 6.1

PostgreSQL

Bcrypt

Tailwind CSS

Gunicorn & WhiteNoise

Render (Déploiement)

Structure du projet

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
├── staticfiles/
└── README.md


Installation en local

1. Cloner le projet

git clone https://github.com/fari-code/Authentification-Sur-Mesure-sous-Django.git
cd Authentification-Sur-Mesure-sous-Django


2. Créer un environnement virtuel

python -m venv env

# Sur Linux / macOS :
source env/bin/activate

# Sur Windows :
env\Scripts\activate


3. Installer les dépendances

pip install -r requirements.txt


4. Configurer les variables d'environnement

Créez un fichier .env à la racine du projet avec le contenu suivant :

SECRET_KEY=ton-secret-key-tres-longue
DEBUG=True

# Base de données (PostgreSQL local ou SQLite)
DATABASE_URL=postgres://user:password@localhost:5432/nom_db

# Configuration Email (Gmail)
EMAIL_HOST_USER=tonemail@gmail.com
EMAIL_HOST_PASSWORD=ton-mot-de-passe-application
DEFAULT_FROM_EMAIL=Authentification <tonemail@gmail.com>

# Google OAuth
GOOGLE_CLIENT_ID=ton-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=ton-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/google/callback/


5. Appliquer les migrations

python manage.py makemigrations
python manage.py migrate


6. Lancer le serveur de développement

python manage.py runserver


Accédez à l'application via : http://127.0.0.1:8000

Configuration de Google OAuth

Accédez à la Google Cloud Console.

Créez un nouveau projet.

Configurez l'écran de consentement OAuth (OAuth consent screen) en choisissant le type External.

Allez dans Credentials > Create Credentials > OAuth Client ID > Web application.

Ajoutez les URI de redirection autorisées (Redirect URIs) :

http://127.0.0.1:8000/google/callback/

http://localhost:8000/google/callback/

Copiez le Client ID et le Client Secret générés dans votre fichier .env.

Déploiement sur Render

Prérequis

Un fichier requirements.txt à la racine.

Un script de build build.sh (si nécessaire pour exécuter les migrations et la collecte des fichiers statiques).

Étapes de déploiement

Publiez le code source sur un dépôt GitHub.

Créez un nouveau Web Service sur Render lié à votre dépôt.

Créez une instance PostgreSQL sur Render (offre gratuite).

Ajoutez les variables d'environnement dans les paramètres de votre service sur Render.

Renseignez les commandes suivantes :

Build Command : ./build.sh

Start Command : gunicorn authentification.wsgi:application

Variables d'environnement pour Render

Clé

Description

SECRET_KEY

Clé secrète de production Django

DEBUG

False

DATABASE_URL

URL de la base de données PostgreSQL Render

EMAIL_HOST_USER

Adresse Gmail pour l'envoi d'emails

EMAIL_HOST_PASSWORD

Mot de passe d'application Gmail

DEFAULT_FROM_EMAIL

Adresse d'expédition affichée

GOOGLE_CLIENT_ID

Identifiant client Google OAuth

GOOGLE_CLIENT_SECRET

Clé secrète client Google OAuth

GOOGLE_REDIRECT_URI

https://ton-app.onrender.com/google/callback/

Email de réinitialisation

Validation du token limitée à 5 minutes.

Modèle d'email au format HTML.

Bouton de réinitialisation sécurisé.

Sécurité

Chiffrement des mots de passe géré avec bcrypt.

Tokens de réinitialisation à usage unique avec expiration automatique.

Protection contre les attaques CSRF.

Saisie et gestion sécurisée des cookies de session (HttpOnly).

Messages d'erreur génériques lors de l'authentification pour prévenir l'énumération des utilisateurs.

Auteur

fari-code

Projet d'authentification personnalisée sous Django.

Licence

Ce projet est distribué sous licence open-source. Vous êtes libre de le modifier et de l'utiliser.