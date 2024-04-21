from firebase_admin import auth
from django.contrib.auth.models import User
from drf_easily_auth.models import Firebase

from typing import List


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