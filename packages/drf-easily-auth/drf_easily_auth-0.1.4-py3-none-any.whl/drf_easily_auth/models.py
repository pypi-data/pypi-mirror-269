from django.db import models
from django.contrib.auth.models import User

# Firebase Admin
class Firebase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField() # Email verified
    sign_in_provider = models.CharField(max_length=255) # Sign in provider
    # ---------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)