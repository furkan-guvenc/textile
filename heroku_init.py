def init():
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate

    admin = authenticate(username='admin', password='adminpw')
    if admin is None:
        user = User.objects.create_superuser(username='admin', password='adminpw', email='admin@admin.com')
        user.save()
