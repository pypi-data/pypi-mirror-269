from rest_framework import authentication
from rest_framework import exceptions
import os

# Firebase Admin
import firebase_admin
from firebase_admin import auth
# Models
from django.contrib.auth.models import User
from .models import Firebase

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        
        # Get token from any scheme (Bearer, JWT, etc.)
        token = auth_header.split(' ').pop()
        try:
            decoded_token = auth.verify_id_token(token, check_revoked=True)

            # Extract user data
            uid = decoded_token['uid']
            aud = decoded_token['aud']
            user_id = decoded_token['user_id']
            email = decoded_token['email']
            email_verified = decoded_token['email_verified']
            provider = decoded_token['firebase']['sign_in_provider']

        except auth.InvalidIdTokenError:
            raise exceptions.AuthenticationFailed('Invalid authentication token.')
        except auth.ExpiredIdTokenError:
            raise exceptions.AuthenticationFailed('Expired authentication token.')
        except auth.RevokedIdTokenError:
            raise exceptions.AuthenticationFailed('Revoked authentication token.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')

        user, created = User.objects.get_or_create(username=user_id, email=email)
        if created:
            # Disable user password
            user.set_unusable_password()
            user.save()

            # Firebase user informations (aud, email_verified, sign_in_provider)
            firebase_user = Firebase.objects.create(
                user=user,
                aud=aud,
                email_verified=email_verified,
                sign_in_provider=provider
            )
        return (user, None)  # authentication successful

