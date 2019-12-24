from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'It adds an admin'

    def handle(self, *args, **options):
        admin = User.objects.create_superuser(username='admin', password='adminpw', email='admin@admin.com')
        admin.save()
