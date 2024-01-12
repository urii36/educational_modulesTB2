import os

from django.core.management import BaseCommand

from config import settings
from users.models import User


class Command(BaseCommand):
    help = 'Reset and add sample payment data to the Payment model'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()

        super_user = User.objects.create(
            email=settings.EMAIL_HOST_USER,
            first_name='Admin',
            last_name='educational_modules',
            is_staff=True,
            is_superuser=True
        )
        super_user.set_password(os.getenv('ADMIN_PASSWORD'))
        super_user.save()