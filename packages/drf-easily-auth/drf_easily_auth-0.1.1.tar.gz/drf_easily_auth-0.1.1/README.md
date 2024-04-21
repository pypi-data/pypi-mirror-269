# DRF Firebase Auth

Ce package permet une integration avec Firebase lors de l'authentification hors du contexte Django.

## 1. Firebase configuration

Créer votre base de donnée [Firebase](https://console.firebase.google.com/), puis télécharger le fichier d'authentification `.json` lié à votre projet.

- Rendez vous dans les `Paramètres de votre projet`
- Puis dans la section `Comptes de service`
- Selectionner `Python` puis télécharger en cliquant sur `Générer une nouvelle clé privée`
- Charger le fichier `.json` dans votre projet Django


## 2. Django configuration

**Install authentication app in project**

```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Insert this app
    'drf_easily_auth',
]

FIREBASE_CONFIG_FILE = # Your Firebase config file path download in step 1
```

**Configuration custom Firebase authentication in rest framework**

```bash
'DEFAULT_AUTHENTICATION_CLASSES': [
    'drf_easily_auth.firebase.FirebaseAuthentication',
],
```

**Sync all existing users from your Firebase database**

```bash
python3 manage.py syncfirebaseusers
```