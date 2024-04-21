from django.apps import AppConfig
from django.conf import settings
import os

# Firebase Admin
import firebase_admin
from firebase_admin import credentials


# Fonction pour vérifier si le fichier firebase.json existe
def check_firebase_file():
    if not os.path.exists(settings.FIREBASE_CONFIG_FILE):
        raise FileNotFoundError("Define the FIREBASE_CONFIG_FILE in settings.py")
  

class DrfEasilyAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "drf_easily_auth"

    def ready(self):
        cred = credentials.Certificate(settings.FIREBASE_CONFIG_FILE)
        firebase_admin.initialize_app(cred)
