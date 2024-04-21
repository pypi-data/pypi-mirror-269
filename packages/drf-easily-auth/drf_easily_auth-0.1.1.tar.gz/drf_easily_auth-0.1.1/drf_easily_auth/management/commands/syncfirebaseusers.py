from django.core.management.base import BaseCommand
from firebase_admin import auth
from django.contrib.auth.models import User
from authentication.models import Firebase  

class Command(BaseCommand):
    """
    Command to synchronise users from Firebase
    
    Usage:
        python3 manage.py syncfirebaseusers
    """
    help = 'Users synchronisation from Firebase'

    def handle(self, *args, **options):
        header_message = """
        ########################################################
        #                                                      #
        #           Firebase User Synchronisation              #
        #                                                      #
        ########################################################
        """
        self.stdout.write(self.style.SUCCESS(header_message))
        firebase_users = auth.list_users().iterate_all()

        for firebase_user in firebase_users:
            user, created = User.objects.get_or_create(username=firebase_user.uid, email=firebase_user.email)
            if created:
                user.set_unusable_password()
                user.save()

                Firebase.objects.create(
                    user=user,
                    email_verified=firebase_user.email_verified,
                    sign_in_provider=firebase_user.provider_id
                )
                self.stdout.write(self.style.SUCCESS(f'User sync > ID: {user.username} > Email: {user.email}'))
        self.stdout.write(self.style.SUCCESS('Users synchronisation completed'))