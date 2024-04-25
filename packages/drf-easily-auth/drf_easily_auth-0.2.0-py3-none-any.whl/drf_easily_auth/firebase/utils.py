from firebase_admin import auth
from django.contrib.auth.models import User
from drf_easily_auth.models import Firebase

from typing import List, Union


def import_users() -> List[User]:
    """
    Import users from Firebase and sync with Django's User model.
    """
    firebase_users = auth.list_users().iterate_all()

    for firebase_user in firebase_users:
        if not firebase_user.email:
            user, created = User.objects.get_or_create(username=firebase_user.uid)
        else:
            user, created = User.objects.get_or_create(username=firebase_user.uid, email=firebase_user.email)

        if created:
            user.set_unusable_password()
            user.save()

            Firebase.objects.create(
                user=user,
                email_verified=firebase_user.email_verified,
                sign_in_provider=firebase_user.provider_id
            )
    return User.objects.all()


# Fonction pour ajouter des informations personnalisées à un utilisateur Firebase
def add_custom_claims(uid: str, claims: dict) -> Union[auth.UserRecord, None]:
    """
    Add custom claims to a Firebase user.
    """
    auth.set_custom_user_claims(uid, claims)
    if auth.get_user(uid).custom_claims == claims:
        # Ici on force la mise à jour du token pour que les nouvelles informations soient prises en compte
        # Ce qui à pour effet deconnecter le user de toutes ses sessions sur tous les devices
        # Il devra se reconnecter pour obtenir un nouveau token
        # Cela assure que les nouvelles informations sont prises en compte rapidement
        auth.revoke_refresh_tokens(uid)
        return auth.get_user(uid)
    return None


